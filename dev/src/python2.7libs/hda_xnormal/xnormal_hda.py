# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
import platform
import subprocess
import hda_xnormal.Python_xNormal.xNormal as xNormal
import shutil
import os
import hou

_is_win = platform.system() == 'Windows'
PROGRAM_FILES = [  # TODO システムから動的に取得したい
    r'C:\Program Files\xNormal',
    # 'C:\Program Files (x86)\xNormal'  # 32bitは未サポート
]
DEFAULT_OUTPUT_DIR = (os.path.expanduser('~') + '\\..\\Desktop').replace('/', '\\')
DEFAULT_WORK_FOLDER = os.path.dirname(__file__)
LOW_MODEL  = os.path.dirname(__file__) + '\\sample_mesh\\low.obj'
HIGH_MODEL = os.path.dirname(__file__) + '\\sample_mesh\\middle.obj'
_work_folder = ''


def _get_work_folder(work_folder, create_if_not_exist=True):
    if not work_folder:
        work_folder = DEFAULT_WORK_FOLDER
    if create_if_not_exist and not os.path.exists(work_folder):
        _makedirs(work_folder)
    return work_folder


def _makedirs(file_path):
    file_path = os.path.dirname(file_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def _get_config_path():
    return _work_folder + '\\xnormal_config.xml'


def run_config(conf):
    config_file = _get_config_path()
    with open(config_file, 'w') as f:
        f.write(conf)
    # cmd = ['"%s"' % xNormal.path, CONFIG_FILE]
    # ret_code = os.system(' '.join(cmd))
    cmd = [xNormal.path, config_file]
    ret_code = subprocess.call(cmd)
    # print(' '.join(cmd))
    if ret_code != 0:
        raise Exception('xnormal export error : {} {}'.format(xNormal.path, config_file))


# hack 呼び出し方を変えると黒いウィンドウが出ない（xnormalのウィンドウは処理中でてしまう）
xNormal.run_config = run_config


def _init_xnormal_module(xnormal_exe_path=''):

    if not xnormal_exe_path:
        pfiles_path = None
        for p in PROGRAM_FILES:
            if os.path.exists(p):
                pfiles_path = p
                break
        if not pfiles_path:
            return False
        dirs = os.listdir(pfiles_path)
        version_digits = [x.split('.') for x in dirs]

        for vd_list in version_digits:
            while len(vd_list) < 3:
                vd_list.append('0')

        def sort_func(x, y):
            if int(x[0]) > int(y[0]):
                return -1
            if int(x[0]) < int(y[0]):
                return 1
            if int(x[1]) > int(y[1]):
                return -1
            if int(x[2]) < int(y[1]):
                return 1
            if int(x[2]) > int(y[2]):
                return -1
            if int(x[2]) < int(y[2]):
                return 1
            return 0
        version_digits.sort(cmp=sort_func)
        latest_install_folder = '.'.join(version_digits[0])
        # xNormal.version = latest_install_folder  # 設定の必要なさそう
        xNormal.path = pfiles_path + '\\' + latest_install_folder + '\\x64\\xNormal.exe'
    else:
        if not os.path.isfile(xnormal_exe_path):
            return False
        xNormal.path = xnormal_exe_path
    return True


def clear_exported_textures(kwargs):
    node = kwargs['node']
    textures = [
        str(node.parm("normal_export_img").eval()),
        str(node.parm("occlusion_export_img").eval())
    ]
    for t in textures:
        if os.path.isfile(t):
            print('removed : {}'.format(t))
            os.remove(t)
    hou.hscript('glcache -c')


def execute(kwargs):
    """
    実際のノード部分
    UIパラメータを調整して xnormal libにつなぐ
    """
    global _work_folder
    node = kwargs['node']

    texture_size = node.parm("texture_size").menuItems()[node.parm("texture_size").eval()]

    normal_export_flag = node.parm("normal_export_flag").eval()
    normal_export_img = ''
    if normal_export_flag:
        normal_export_img = str(node.parm("normal_export_img").eval())

    export_occlusion_flag = node.parm("export_occlusion_flag").eval()
    occlusion_export_img = ''
    if export_occlusion_flag:
        occlusion_export_img = str(node.parm("occlusion_export_img").eval())

    work_folder_candidate = str(node.parm("work_dir").eval())

    xnormal_auto_search = node.parm("xnormal_auto_search").eval()
    xnormal_exe_path = ''
    if xnormal_auto_search:
        xnormal_exe_path = str(node.parm("xnormal_exe_path").eval())

    temp_file_prefix = node.name()

    high_model_path = str(node.parm("high_mesh_file/file").eval())
    low_model_path = str(node.parm("low_mesh_file/file").eval())

    if not os.path.isfile(high_model_path):
        raise Exception('temp high mesh file not exported : {}'.format(high_model_path))
    if not os.path.isfile(low_model_path):
        raise Exception('temp low mesh file not exported : {}'.format(low_model_path))

    normals_x_y_z = node.parmTuple("normals_x_y_z").eval()

    gen_normals = False
    if normal_export_img:
        gen_normals = True
    gen_ao = False
    if occlusion_export_img:
        gen_ao = True
    if not gen_normals and not gen_ao:
        return

    try:
        _work_folder = \
            _get_work_folder(work_folder_candidate, create_if_not_exist=True)  # run_configのhack処理のためglobalに保存
    except Exception:
        raise('work folder creation error: {}'.format(work_folder_candidate))

    if _work_folder == '' or not os.path.exists(_work_folder) or not os.path.isdir(_work_folder):
        raise('work folder not exist : {}'.format(_work_folder))

    ok = _init_xnormal_module(xnormal_exe_path)
    if not ok:
        raise Exception('Invalid xnormal setting.')
    temp_out_file  = _work_folder + '\{}_out.png'.format(temp_file_prefix)

    # lib 呼び出し
    xNormal.run(
        high_model_path,
        low_model_path,
        temp_out_file,
        width=texture_size,
        height=texture_size,
        gen_normals=gen_normals,
        gen_ao=gen_ao,
        closest_if_fails=int(node.parm("normal_closest_if_fails").eval()) == 1,
        aa=int(node.parm("normal_aa").eval()),
        tangent_space=int(node.parm("normal_tangent_space").eval()) == 1,
        discard_backface_hits=int(node.parm("normal_discard_backface_hits").eval()) == 1,
        normals_x=str(normals_x_y_z[0]),
        normals_y=str(normals_x_y_z[1]),
        normals_z=str(normals_x_y_z[2]),
        normals_high_texture=int(node.parm("normals_high_texture").eval()) == 1,
        normals_high_matid=int(node.parm("normals_high_matid").eval()) == 1,

        # TODO ao params

    )
    temp_files = [
        _get_config_path()
    ]

    # 一時ファイル名で書き出したテクスチャを要望の名前に変更してコピー
    texture_generated = False
    if gen_normals:
        normal_out_file = _work_folder + '\\{}_out_normals.png'.format(temp_file_prefix)  # 実際に書き出される名前
        temp_files.append(normal_out_file)
        _makedirs(normal_export_img)
        if os.path.exists(normal_export_img):
            os.remove(normal_export_img)
        shutil.copy(normal_out_file, normal_export_img)
        texture_generated = True
    if gen_ao:
        ao_out_file = _work_folder + '\\{}_out_occlusion.png'.format(temp_file_prefix)  # 実際に書き出される名前
        temp_files.append(ao_out_file)
        _makedirs(occlusion_export_img)
        if os.path.exists(occlusion_export_img):
            os.remove(occlusion_export_img)
        shutil.copy(ao_out_file, occlusion_export_img)
        texture_generated = True

    # テクスチャのキャッシュクリア（マテリアルの適用はSOP内で対応)
    apply_preview_material = int(node.parm('apply_preview_material').eval()) == 1
    clear_cache_after_export = int(node.parm('clear_cache_after_export').eval()) == 1
    if texture_generated and apply_preview_material and clear_cache_after_export:
        hou.hscript('glcache -c')
        # print('GL cahce cleared')
    # 一時ファイルの削除 (キャッシュのobjファイルは動作が不安定にならないよう残している)
    delete_temp_files = int(node.parm('delete_temp_files').eval()) == 1
    if delete_temp_files:
        for f in temp_files:
            if f and os.path.isfile(f):
                # print('removing {}'.format(f))
                os.remove(f)
