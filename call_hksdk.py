import ctypes
import os
import logging
# import hkws.model.login as login
# import hkws.model.preview as preview
#
# from hkws.callback import hikFunc
#
# from hkws.callback import g_real_data_call_back


class HKAdapter:
    so_list = [""]

    # 加载目录下所有so文件
    def add_lib(self, path, suffix):
        files = os.listdir(path)
        for file in files:
            if not os.path.isdir(path + file):
                if file.endswith(suffix):
                    self.so_list.append(path + file)
            else:
                self.add_lib(path + file + "/", suffix)

    # python 调用 sdk 指定方法
    def call_cpp(self, func_name, *args):
        for so_lib in self.so_list:
            try:
                lib = ctypes.cdll.LoadLibrary(so_lib)
                try:
                    value = eval("lib.%s" % func_name)(*args)
                    logging.info("调用的库：" + so_lib)
                    logging.info("执行成功,返回值：" + str(value))
                    return value
                except:
                    continue
            except:
                continue
            # logging.info("库文件载入失败：" + so_lib )
        logging.error("没有找到接口！")
        return False

    # 初始化海康微视 sdk
    def init_sdk(self):
        init_res = self.call_cpp("NET_DVR_Init")  # SDK初始化
        if init_res:
            logging.info("SDK初始化成功")
            return True
        else:
            error_info = self.call_cpp("NET_DVR_GetLastError")
            logging.error("SDK初始化错误：" + str(error_info))
            return False

    # 释放sdk
    def sdk_clean(self):
        result = self.call_cpp("NET_DVR_Cleanup")
        logging.info("释放资源", result)

