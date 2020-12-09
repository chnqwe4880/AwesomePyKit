# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtCore import (
    QSize,
    Qt,
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QIcon,
    QMovie,
)
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from interface import *
from library import *
from library.libm import PyEnv


class MainInterfaceWindow(Ui_MainInterface, QMainWindow):
    def __init__(self):
        super(MainInterfaceWindow, self).__init__()
        self.setupUi(self)
        self._binding()

    def _binding(self):
        self.about.triggered.connect(self._show_about)
        self.description.triggered.connect(self._show_usinghelp)
        self.btn_manPacks.clicked.connect(self._show_pkgmgr)
        self.btn_setIndex.clicked.connect(self._show_indexmgr)

    @staticmethod
    def _show_about():
        try:
            with open('help/About.html', encoding='utf-8') as help_html:
                info = help_html.read()
                icon = QMessageBox.Information
        except Exception:
            info = '"关于"信息文件(help/About.html)已丢失。'
            icon = QMessageBox.Critical
        about_panel = NewMessageBox('关于', info, icon)
        about_panel.get_role()

    @staticmethod
    def _show_usinghelp():
        information_panel_window.setWindowTitle('使用帮助')
        try:
            with open('help/UsingHelp.html', encoding='utf-8') as using_html:
                information_panel_window.help_panel.setText(using_html.read())
        except Exception:
            information_panel_window.help_panel.setText(
                '"使用帮助"文件(help/UsingHelp.html)已丢失。'
            )
        information_panel_window.setGeometry(430, 100, 0, 0)
        information_panel_window.show()

    @staticmethod
    def _show_pkgmgr():
        package_manager_window.show()

    @staticmethod
    def _show_indexmgr():
        mirror_source_manager_window.show()


class PackageManagerWindow(Ui_PackageManager, QMainWindow):
    def __init__(self):
        super(PackageManagerWindow, self).__init__()
        self.setupUi(self)
        self._setupOthers()
        self._binding()
        self.running_threads = []
        self.cur_pkgs_info = {}
        self._reverseds = [True, True, True, True]
        self._py_envs_list = get_pyenv_list(load_conf('pths'))
        self._py_paths_list = [
            py_env.env_path for py_env in self._py_envs_list
        ]

    def _setupOthers(self):
        self.tw_installed_info.setColumnWidth(0, 220)
        self.tw_installed_info.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.tw_installed_info.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Interactive
        )
        self.tw_installed_info.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.tw_installed_info.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        self.loading_mov = QMovie(os.path.join(sources_path, 'loading.gif'))
        self.loading_mov.setScaledSize(QSize(15, 15))

    def show(self):
        super().show()
        self.list_widget_pyenvs_update()
        self.lw_py_envs.setCurrentRow(0)

    def closeEvent(self, event):
        self._stop_running_thread()
        self.clear_table_widget()
        save_conf(self._py_paths_list, 'pths')
        event.accept()

    def start_loading(self, text):
        self.lb_loading_tip.clear()
        self.lb_loading_tip.setText(text)
        self.lb_loading_gif.clear()
        self.lb_loading_gif.setMovie(self.loading_mov)
        self.loading_mov.start()

    def stop_loading(self):
        self.loading_mov.stop()
        self.lb_loading_gif.clear()
        self.lb_loading_tip.clear()

    def showMessage(self, text):
        self.lb_loading_tip.setText(text)

    def clean_finished_thread(self):
        for index, thread in enumerate(self.running_threads):
            if thread.isFinished():
                self.running_threads.pop(index)

    def _stop_running_thread(self):
        for thread in self.running_threads:
            thread.exit()

    def _binding(self):
        self.btn_autosearch.clicked.connect(self._auto_search_py_envs)
        self.btn_delselected.clicked.connect(self._del_selected)
        self.btn_addmanully.clicked.connect(self._add_py_path_manully)
        self.cb_check_uncheck_all.clicked.connect(self._select_all_none)
        self.lw_py_envs.itemPressed.connect(lambda: self._get_pkgs_info(0))
        self.btn_check_for_updates.clicked.connect(self._check_for_updates)
        self.btn_install_package.clicked.connect(self.install_pkgs)
        self.btn_uninstall_package.clicked.connect(self.uninstall_pkgs)
        self.btn_upgrade_package.clicked.connect(self.upgrade_pkgs)
        self.btn_upgrade_all.clicked.connect(self.upgrade_all)
        self.tw_installed_info.horizontalHeader().sectionClicked[int].connect(
            self.sort_by_column
        )

    def list_widget_pyenvs_update(self):
        row_size = QSize(0, 30)
        cur_py_env_index = self.lw_py_envs.currentRow()
        self.lw_py_envs.clear()
        for py_env in self._py_envs_list:
            item = QListWidgetItem(str(py_env))
            item.setSizeHint(row_size)
            self.lw_py_envs.addItem(item)
        if cur_py_env_index != -1:
            self.lw_py_envs.setCurrentRow(cur_py_env_index)

    def table_widget_pkgs_info_update(self):
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(len(self.cur_pkgs_info))
        color_green = QColor(0, 170, 0)
        color_red = QColor(255, 0, 0)
        color_gray = QColor(243, 243, 243)
        for rowind, pkg_name in enumerate(self.cur_pkgs_info):
            even_num_row = rowind % 2
            item = QTableWidgetItem(pkg_name)
            self.tw_installed_info.setItem(rowind, 0, item)
            if not even_num_row:
                item.setBackground(color_gray)
            for colind, item_text in enumerate(
                self.cur_pkgs_info.get(pkg_name, ['', '', ''])
            ):
                item = QTableWidgetItem(item_text)
                if colind == 2:
                    if item_text in ('升级成功', '卸载成功'):
                        item.setForeground(color_green)
                    elif item_text in ('升级失败', '卸载失败'):
                        item.setForeground(color_red)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                if not even_num_row:
                    item.setBackground(color_gray)
                self.tw_installed_info.setItem(rowind, colind + 1, item)

    def sort_by_column(self, colind):
        if colind == 0:
            self.cur_pkgs_info = dict(
                sorted(
                    self.cur_pkgs_info.items(),
                    key=lambda x: x[0].lower(),
                    reverse=self._reverseds[colind],
                )
            )
        else:
            self.cur_pkgs_info = dict(
                sorted(
                    self.cur_pkgs_info.items(),
                    key=lambda x: x[1][colind - 1],
                    reverse=self._reverseds[colind],
                )
            )
        self.table_widget_pkgs_info_update()
        self._reverseds[colind] = not self._reverseds[colind]

    def clear_table_widget(self):
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(0)

    def _get_pkgs_info(self, no_connect):
        index_selected = self.lw_py_envs.currentRow()
        if index_selected == -1:
            return

        def do_get_pkgs_info():
            pkgs_info = self._py_envs_list[index_selected].pkgs_info()
            self.cur_pkgs_info.clear()
            for pkg_info in pkgs_info:
                self.cur_pkgs_info[pkg_info[0]] = [pkg_info[1], '', '']

        thread_get_pkgs_info = NewTask(do_get_pkgs_info)
        if not no_connect:
            thread_get_pkgs_info.started.connect(self.lock_widgets)
            thread_get_pkgs_info.started.connect(
                lambda: self.start_loading('正在加载包信息...')
            )
            thread_get_pkgs_info.finished.connect(
                self.table_widget_pkgs_info_update
            )
            thread_get_pkgs_info.finished.connect(self.stop_loading)
            thread_get_pkgs_info.finished.connect(self.release_widgets)
            thread_get_pkgs_info.finished.connect(self.clean_finished_thread)
        thread_get_pkgs_info.start()
        self.running_threads.append(thread_get_pkgs_info)

    def indexs_selected_row(self):
        row_indexs = []
        for item in self.tw_installed_info.selectedItems():
            row_index = item.row()
            if row_index not in row_indexs:
                row_indexs.append(row_index)
        return row_indexs

    def _select_all_none(self):
        is_checked = self.cb_check_uncheck_all.isChecked()
        if is_checked:
            self.tw_installed_info.selectAll()
        else:
            self.tw_installed_info.clearSelection()

    def _auto_search_py_envs(self):
        def search_envs():
            for py_path in all_py_paths():
                if py_path in self._py_paths_list:
                    continue
                try:
                    py_env = PyEnv(py_path)
                except Exception:
                    continue
                self._py_envs_list.append(py_env)
                self._py_paths_list.append(py_env.env_path)

        thread_search_envs = NewTask(search_envs)
        thread_search_envs.started.connect(self.lock_widgets)
        thread_search_envs.started.connect(
            lambda: self.start_loading('正在搜索Python目录...')
        )
        thread_search_envs.finished.connect(self.clear_table_widget)
        thread_search_envs.finished.connect(self.list_widget_pyenvs_update)
        thread_search_envs.finished.connect(self.stop_loading)
        thread_search_envs.finished.connect(self.release_widgets)
        thread_search_envs.finished.connect(self.clean_finished_thread)
        thread_search_envs.finished.connect(
            lambda: save_conf(self._py_paths_list, 'pths')
        )
        thread_search_envs.start()
        self.running_threads.append(thread_search_envs)

    def _del_selected(self):
        cur_index = self.lw_py_envs.currentRow()
        if cur_index == -1:
            return
        del self._py_envs_list[cur_index]
        del self._py_paths_list[cur_index]
        self.lw_py_envs.removeItemWidget(self.lw_py_envs.takeItem(cur_index))
        self.clear_table_widget()
        save_conf(self._py_paths_list, 'pths')

    def _add_py_path_manully(self):
        input_dialog = NewInputDialog(
            self, 560, 0, '添加Python目录', '请输入Python目录路径：'
        )
        py_path, ok = input_dialog.getText()
        if not (ok and py_path):
            return
        if not check_py_path(py_path):
            return self.showMessage('无效的Python目录路径！')
        py_path = os.path.join(py_path, '')
        if py_path in self._py_paths_list:
            return self.showMessage('要添加的Python目录已存在。')
        py_env = PyEnv(py_path)
        self._py_envs_list.append(py_env)
        self._py_paths_list.append(py_env.env_path)
        self.list_widget_pyenvs_update()
        save_conf(self._py_paths_list, 'pths')

    def _check_for_updates(self):
        if self.tw_installed_info.rowCount() == 0:
            return
        cur_row = self.lw_py_envs.currentRow()
        if cur_row == -1:
            return
        self._get_pkgs_info(no_connect=1)

        def do_get_outdated():
            if self.running_threads:
                self.running_threads[0].wait()
            outdateds = self._py_envs_list[cur_row].outdated()
            for outdated_info in outdateds:
                self.cur_pkgs_info.setdefault(outdated_info[0], ['', '', ''])[
                    1
                ] = outdated_info[2]

        thread_get_outdated = NewTask(do_get_outdated)
        thread_get_outdated.started.connect(self.lock_widgets)
        thread_get_outdated.started.connect(
            lambda: self.start_loading('正在检查更新，请耐心等待...')
        )
        thread_get_outdated.finished.connect(
            self.table_widget_pkgs_info_update
        )
        thread_get_outdated.finished.connect(self.stop_loading)
        thread_get_outdated.finished.connect(self.release_widgets)
        thread_get_outdated.finished.connect(self.clean_finished_thread)
        thread_get_outdated.start()
        self.running_threads.append(thread_get_outdated)

    def lock_widgets(self):
        for widget in (
            self.btn_autosearch,
            self.btn_addmanully,
            self.btn_delselected,
            self.lw_py_envs,
            self.tw_installed_info,
            self.cb_check_uncheck_all,
            self.btn_check_for_updates,
            self.btn_install_package,
            self.btn_uninstall_package,
            self.btn_upgrade_package,
            self.btn_upgrade_all,
        ):
            widget.setEnabled(False)

    def release_widgets(self):
        for widget in (
            self.btn_autosearch,
            self.btn_addmanully,
            self.btn_delselected,
            self.lw_py_envs,
            self.tw_installed_info,
            self.cb_check_uncheck_all,
            self.btn_check_for_updates,
            self.btn_install_package,
            self.btn_uninstall_package,
            self.btn_upgrade_package,
            self.btn_upgrade_all,
        ):
            widget.setEnabled(True)

    def install_pkgs(self):
        cur_py_env = self._py_envs_list[self.lw_py_envs.currentRow()]
        pkgs_to_install = NewInputDialog(
            self, title='安装', label=f'注：多个名称请用空格隔开\n安装目标：{cur_py_env}',
        )
        names, ok = pkgs_to_install.getText()
        names = [name for name in names.split() if name]
        if not (names and ok):
            return

        def do_install():
            for _ in loop_install(cur_py_env, names):
                pass

        thread_install_pkgs = NewTask(do_install)
        thread_install_pkgs.started.connect(self.lock_widgets)
        thread_install_pkgs.started.connect(
            lambda: self.start_loading('正在安装，请稍候...')
        )
        thread_install_pkgs.finished.connect(lambda: self._get_pkgs_info(0))
        thread_install_pkgs.finished.connect(self.stop_loading)
        thread_install_pkgs.finished.connect(self.clean_finished_thread)
        thread_install_pkgs.start()
        self.running_threads.append(thread_install_pkgs)

    def uninstall_pkgs(self):
        cur_pkgs_info_keys = tuple(self.cur_pkgs_info.keys())
        pkg_indexs = self.indexs_selected_row()
        pkg_names = [cur_pkgs_info_keys[index] for index in pkg_indexs]
        if not pkg_names:
            return
        cur_py_env = self._py_envs_list[self.lw_py_envs.currentRow()]
        len_pkgs = len(pkg_names)
        names_text = (
            '\n'.join(pkg_names)
            if len_pkgs <= 10
            else '\n'.join(('\n'.join(pkg_names[:10]), '......'))
        )
        uninstall_msg_box = QMessageBox(
            QMessageBox.Question, '卸载', f'确认卸载？\n{names_text}'
        )
        uninstall_msg_box.addButton('确定', QMessageBox.AcceptRole)
        reject = uninstall_msg_box.addButton('取消', QMessageBox.RejectRole)
        uninstall_msg_box.setDefaultButton(reject)
        if uninstall_msg_box.exec() != 0:
            return

        def do_uninstall():
            for pkg_name, code in loop_uninstall(cur_py_env, pkg_names):
                item = self.cur_pkgs_info.setdefault(pkg_name, ['', '', ''])
                if code:
                    item[2] = '卸载成功'
                else:
                    item[2] = '卸载失败'

        thread_uninstall_pkgs = NewTask(do_uninstall)
        thread_uninstall_pkgs.started.connect(self.lock_widgets)
        thread_uninstall_pkgs.started.connect(
            lambda: self.start_loading('正在卸载，请稍候...')
        )
        thread_uninstall_pkgs.finished.connect(
            self.table_widget_pkgs_info_update
        )
        thread_uninstall_pkgs.finished.connect(self.stop_loading)
        thread_uninstall_pkgs.finished.connect(self.release_widgets)
        thread_uninstall_pkgs.finished.connect(self.clean_finished_thread)
        thread_uninstall_pkgs.start()
        self.running_threads.append(thread_uninstall_pkgs)

    def upgrade_pkgs(self):
        cur_pkgs_info_keys = tuple(self.cur_pkgs_info.keys())
        pkg_indexs = self.indexs_selected_row()
        pkg_names = [cur_pkgs_info_keys[index] for index in pkg_indexs]
        if not pkg_names:
            return
        cur_py_env = self._py_envs_list[self.lw_py_envs.currentRow()]
        len_pkgs = len(pkg_names)
        names_text = (
            '\n'.join(pkg_names)
            if len_pkgs <= 10
            else '\n'.join(('\n'.join(pkg_names[:10]), '......'))
        )
        uninstall_msg_box = QMessageBox(
            QMessageBox.Question, '升级', f'确认升级？\n{names_text}'
        )
        uninstall_msg_box.addButton('确定', QMessageBox.AcceptRole)
        reject = uninstall_msg_box.addButton('取消', QMessageBox.RejectRole)
        uninstall_msg_box.setDefaultButton(reject)
        if uninstall_msg_box.exec() != 0:
            return

        def do_upgrade():
            for pkg_name, code in loop_install(
                cur_py_env, pkg_names, upgrade=1
            ):
                item = self.cur_pkgs_info.setdefault(pkg_name, ['', '', ''])
                if code:
                    item[2] = '升级成功'
                else:
                    item[2] = '升级失败'

        thread_upgrade_pkgs = NewTask(do_upgrade)
        thread_upgrade_pkgs.started.connect(self.lock_widgets)
        thread_upgrade_pkgs.started.connect(
            lambda: self.start_loading('正在升级，请稍候...')
        )
        thread_upgrade_pkgs.finished.connect(
            self.table_widget_pkgs_info_update
        )
        thread_upgrade_pkgs.finished.connect(self.stop_loading)
        thread_upgrade_pkgs.finished.connect(self.release_widgets)
        thread_upgrade_pkgs.finished.connect(self.clean_finished_thread)
        thread_upgrade_pkgs.start()
        self.running_threads.append(thread_upgrade_pkgs)

    def upgrade_all(self):
        upgradeable = [
            item[0] for item in self.cur_pkgs_info.items() if item[1][1]
        ]
        if not upgradeable:
            msg_box = QMessageBox(
                QMessageBox.Information, '提示', '请先检查更新确认是否有可更新的包。'
            )
            msg_box.addButton('确定', QMessageBox.AcceptRole)
            msg_box.exec()
            return
        cur_py_env = self._py_envs_list[self.lw_py_envs.currentRow()]
        len_pkgs = len(upgradeable)
        names_text = (
            '\n'.join(upgradeable)
            if len_pkgs <= 10
            else '\n'.join(('\n'.join(upgradeable[:10]), '......'))
        )
        upgrade_all_msg_box = QMessageBox(
            QMessageBox.Question, '全部升级', f'确认升级？\n{names_text}'
        )
        upgrade_all_msg_box.addButton('确定', QMessageBox.AcceptRole)
        reject = upgrade_all_msg_box.addButton('取消', QMessageBox.RejectRole)
        upgrade_all_msg_box.setDefaultButton(reject)
        if upgrade_all_msg_box.exec() != 0:
            return

        def do_upgrade():
            for pkg_name, code in loop_install(
                cur_py_env, upgradeable, upgrade=1
            ):
                item = self.cur_pkgs_info.setdefault(pkg_name, ['', '', ''])
                if code:
                    item[2] = '升级成功'
                else:
                    item[2] = '升级失败'

        thread_upgrade_pkgs = NewTask(do_upgrade)
        thread_upgrade_pkgs.started.connect(self.lock_widgets)
        thread_upgrade_pkgs.started.connect(
            lambda: self.start_loading('正在升级，请稍候...')
        )
        thread_upgrade_pkgs.finished.connect(
            self.table_widget_pkgs_info_update
        )
        thread_upgrade_pkgs.finished.connect(self.stop_loading)
        thread_upgrade_pkgs.finished.connect(self.release_widgets)
        thread_upgrade_pkgs.finished.connect(self.clean_finished_thread)
        thread_upgrade_pkgs.start()
        self.running_threads.append(thread_upgrade_pkgs)


class MirrorSourceManagerWindow(Ui_MirrorSourceManager, QMainWindow):
    def __init__(self):
        super(MirrorSourceManagerWindow, self).__init__()
        self.setupUi(self)
        self._urls_dict = load_conf('urls')
        self._binding()

    def show(self):
        super(MirrorSourceManagerWindow, self).show()
        self._list_widget_urls_update()

    @staticmethod
    def _widget_for_list_item(url):
        item_layout = QHBoxLayout()
        item_layout.addWidget(QLabel(''))
        item_layout.addWidget(QLabel(url))
        item_layout.setStretch(0, 2)
        item_layout.setStretch(1, 8)
        item_widget = QWidget()
        item_widget.setLayout(item_layout)
        return item_widget

    def _list_widget_urls_update(self):
        self.li_indexurls.clear()
        for name, url in self._urls_dict.items():
            item_widget = self._widget_for_list_item(url)
            li_item = QListWidgetItem()
            li_item.setSizeHint(QSize(560, 42))
            li_item.setText(name)
            self.li_indexurls.addItem(li_item)
            self.li_indexurls.setItemWidget(li_item, item_widget)

    def _binding(self):
        self.btn_clearle.clicked.connect(self._clear_line_edit)
        self.btn_saveurl.clicked.connect(self._save_index_urls)
        self.btn_delurl.clicked.connect(self._del_index_url)
        self.li_indexurls.clicked.connect(self._set_url_line_edit)
        self.btn_setindex.clicked.connect(self._set_global_index_url)
        self.btn_refresh_effective.clicked.connect(self._display_effective_url)

    def _set_url_line_edit(self):
        item = self.li_indexurls.currentItem()
        if (self.li_indexurls.currentRow() == -1) or (not item):
            return
        text = item.text()
        self.le_urlname.setText(text)
        self.le_indexurl.setText(self._urls_dict.get(text, ''))

    def _clear_line_edit(self):
        self.le_urlname.clear()
        self.le_indexurl.clear()

    def _check_name_url(self, name, url):
        if not name:
            self.showMessage('名称不能为空！')
            return False
        if not url:
            self.showMessage('地址不能为空！')
            return False
        if not check_index_url(url):
            self.showMessage('无效的镜像源地址！')
            return False
        if name in self._urls_dict:
            self.showMessage(f'名称<{name}>已存在！')
            return False
        return True

    def _save_index_urls(self):
        name = self.le_urlname.text()
        url = self.le_indexurl.text()
        if self._check_name_url(name, url):
            self._urls_dict[name] = url
        self._list_widget_urls_update()
        save_conf(self._urls_dict, 'urls')

    def _del_index_url(self):
        item = self.li_indexurls.currentItem()
        if (self.li_indexurls.currentRow() == -1) or (not item):
            self.showMessage('没有选中列表内的任何条目。')
            return
        del self._urls_dict[item.text()]
        self._list_widget_urls_update()
        save_conf(self._urls_dict, 'urls')

    def _get_cur_pyenv(self):
        '''使用系统环境变量PATH中第一个Python路径生成一个PyEnv实例。'''
        py_paths = load_conf('pths')
        if not py_paths:
            try:
                return PyEnv(cur_py_path())
            except Exception:
                self.showMessage('没有找到pip可执行文件，请在"包管理器"界面添加任意Python目录到列表。')
        else:
            for py_path in py_paths:
                try:
                    return PyEnv(py_path)
                except Exception:
                    continue
            else:
                self.showMessage('没有找到pip可执行程序，请在"包管理器"界面添加Python目录到列表。')

    def _set_global_index_url(self):
        url = self.le_indexurl.text()
        if not url:
            self.showMessage('要设置为全局镜像源的地址不能为空！')
            return
        if not check_index_url(url):
            self.showMessage('镜像源地址不符合pip镜像源地址格式。')
            return
        pyenv = self._get_cur_pyenv()
        if not pyenv:
            self.showMessage('镜像源启用失败，未找到pip可执行文件。')
            return
        pyenv.set_global_index(url)
        self.showMessage(f'已将"{url}"设置为全局镜像源地址。')

    def _display_effective_url(self):
        pyenv = self._get_cur_pyenv()
        if pyenv:
            self.le_effectiveurl.setText(
                pyenv.get_global_index() or '当前全局镜像源地址为空。'
            )
        else:
            self.le_effectiveurl.setText('无法获取当前全局镜像源地址。')


class InformationPanelWindow(Ui_InformationPanel, QWidget):
    def __init__(self):
        super(InformationPanelWindow, self).__init__()
        self.setupUi(self)

    def closeEvent(self, event):
        self.resize(1, 1)


class NewInputDialog(QInputDialog):
    def __init__(self, parent, sw=560, sh=0, title='', label=''):
        super(NewInputDialog, self).__init__(parent)
        self.resize(sw, sh)
        self.setFont(QFont('Microsoft YaHei UI'))
        self.setWindowTitle(title)
        self.setLabelText(label)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setOkButtonText('确定')
        self.setCancelButtonText('取消')
        self._confirm = self.exec()

    def getText(self):
        return self.textValue(), self._confirm


class NewMessageBox(QMessageBox):
    def __init__(
        self, title, message, icon=QMessageBox.Information, buttons=('accept',)
    ):
        super().__init__(icon, title, message)
        for btn in buttons:
            if btn == 'accept':
                self.addButton('确定', QMessageBox.AcceptRole)
            elif btn == 'reject':
                self.addButton('取消', QMessageBox.RejectRole)
            elif btn == 'destructive':
                self.addButton('拒绝', QMessageBox.DestructiveRole)

    def get_role(self):
        return self.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(sources_path, 'icon.ico')))
    information_panel_window = InformationPanelWindow()
    main_interface_window = MainInterfaceWindow()
    package_manager_window = PackageManagerWindow()
    mirror_source_manager_window = MirrorSourceManagerWindow()
    main_interface_window.show()
    sys.exit(app.exec_())