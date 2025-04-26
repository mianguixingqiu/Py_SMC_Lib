#本库用于使用smc官方提供的dll文件，实现python驱动smc运动控制器的功能。
#本库的所有函数名均将官方smc去掉，其它均相同。
#本库的所有函数均返回一个数值，0代表成功，其他数值代表失败。官方也没给出具体的错误码。
#本库的参数顺序与官方文档相同，改为全小写带下划线的形式。
#使用本库时，需要将LTSMC.dll文件放在与本文件相同的目录下。
#使用本库时，需要安装ctypes库。

import ctypes, os
from ctypes import wintypes

class SMCController:
    def __init__(self):
        # 加载 DLL 文件
        self.smc_dll = ctypes.CDLL(os.path.join(os.getcwd(), 'LTSMC.dll'))
        self._setup_functions()

    def _setup_functions(self):
        # 端口连接
        self.smc_dll.smc_board_init.argtypes = [wintypes.WORD, wintypes.WORD, ctypes.c_char_p, wintypes.DWORD]
        self.smc_dll.smc_board_init.restype = ctypes.c_short
        
        # 断开连接
        self.smc_dll.smc_board_close.argtypes = [wintypes.DWORD]
        self.smc_dll.smc_board_close.restype = ctypes.c_short
        
        #读取当前指令位置计数器值
        self.smc_dll.smc_get_position_unit.argtypes = [wintypes.WORD, wintypes.WORD, ctypes.POINTER(ctypes.c_double)]
        self.smc_dll.smc_get_position_unit.restype = ctypes.c_short
        # 使能指定轴的输出
        self.smc_dll.smc_write_sevon_pin.argtypes = [wintypes.WORD, wintypes.WORD, wintypes.WORD]
        self.smc_dll.smc_write_sevon_pin.restype = ctypes.c_short
        
        # 运行BASIC程序
        self.smc_dll.smc_basic_run.argtypes = [wintypes.WORD]
        self.smc_dll.smc_basic_run.restype = ctypes.c_short
        # 停止BASIC程序
        self.smc_dll.smc_basic_stop.argtypes = [wintypes.WORD]
        self.smc_dll.smc_basic_stop.restype = ctypes.c_short

        # 设置回原点速度参数 
        self.smc_dll.smc_set_home_profile_unit.argtypes =[wintypes.WORD, wintypes.WORD,wintypes.DOUBLE,wintypes.DOUBLE,wintypes.DOUBLE,wintypes.DOUBLE]
        self.smc_dll.smc_set_home_profile_unit.restype = ctypes.c_short
        
        #设置回原点完成后的偏移位置值
        self.smc_dll.smc_set_home_position_unit.argtypes ==[wintypes.WORD, wintypes.WORD, wintypes.WORD, wintypes.DOUBLE]
        self.smc_dll.smc_set_home_position_unit.restype = ctypes.c_short

        # 设置回原点方式
        self.smc_dll.smc_set_homemode.argtypes =[wintypes.WORD, wintypes.WORD, wintypes.WORD, wintypes.DOUBLE, wintypes.WORD, wintypes.WORD]
        self.smc_dll.smc_set_homemode.restype = ctypes.c_short
        # 获取回零点方式
        self.smc_dll.smc_get_homemode.argtypes =[
            wintypes.WORD, wintypes.WORD,
            ctypes.POINTER(wintypes.WORD),
            ctypes.POINTER(ctypes.c_double),
            ctypes.POINTER(wintypes.WORD),
            ctypes.POINTER(wintypes.WORD)]
        self.smc_dll.smc_get_homemode.restype = ctypes.c_short

        # 按指定的方向和速度方式开始回原点 
        self.smc_dll.smc_home_move.argtypes =[wintypes.WORD, wintypes.WORD]
        self.smc_dll.smc_home_move.restype = ctypes.c_short
        
        #PTT模式
        self.smc_dll.smc_ptt_table_unit.argtypes =[
            wintypes.WORD, wintypes.WORD, wintypes.DWORD,
            ctypes.POINTER(ctypes.c_double*100),
            ctypes.POINTER(ctypes.c_double*100)]
        self.smc_dll.smc_ptt_table_unit.restype = ctypes.c_short

        #PTS模式
        self.smc_dll.smc_pts_table_unit.argtypes =[
            wintypes.WORD, wintypes.WORD, wintypes.DWORD,
            ctypes.POINTER(ctypes.c_double*1000),
            ctypes.POINTER(ctypes.c_double*1000),
            ctypes.POINTER(ctypes.c_double*1000)]
        
        #启动PVT运动
        self.smc_dll.smc_pvt_move.argtypes =[wintypes.WORD, wintypes.WORD,ctypes.POINTER(wintypes.WORD)]
        self.smc_dll.smc_pvt_move.restype = ctypes.c_short

        #单轴软着陆功能
        self.smc_dll.smc_t_pmove_extern_unit.argtypes=[
            wintypes.WORD, wintypes.WORD, 
            wintypes.DOUBLE, wintypes.DOUBLE, wintypes.DOUBLE, wintypes.DOUBLE, 
            wintypes.DOUBLE, wintypes.DOUBLE,wintypes.DOUBLE, wintypes.DOUBLE, wintypes.WORD]
        self.smc_dll.smc_t_pmove_extern_unit.restype = ctypes.c_short
        
    def board_init(self, connect_no, type_val, connect_string, baud):
        if isinstance(connect_string, str):
            connect_string = connect_string.encode('utf-8')
        return self.smc_dll.smc_board_init(connect_no, type_val, connect_string, baud)

    def board_close(self, connect_no):
        return self.smc_dll.smc_board_close(connect_no)

    def get_position_unit(self, connect_no, axis):
        # 获取当前指令位置计数器值
        # connect_no: 指定链接号
        # axis: 指定轴号
        # position: 返回当前指令位置计数器值
        position = ctypes.c_double()
        result = self.smc_dll.smc_get_position_unit(connect_no, axis, ctypes.byref(position))
        return result, position.value
    

    def write_sevon_pin(self, connect_no, axis, on_off):
        return self.smc_dll.smc_write_sevon_pin(connect_no, axis, on_off)

    def basic_run(self, connect_no):
        return self.smc_dll.smc_basic_run(connect_no)
    def basic_stop(self, connect_no):
        return self.smc_dll.smc_basic_stop(connect_no)
    #回原点有关函数
    def set_home_profile_unit(self, connect_no, axis, low_vel, high_vel, tacc, tdec ):#设置回原点速度参数
        #connect_no:指定链接号
        #axis:指定轴号
        #low_vel:指定回原点起始速度
        #high_vel指定回原点运行速度
        #tacc设置回原点加速、减速时间，单位s
        #tdec保留值

        return self.smc_dll.smc_set_home_profile_unit(connect_no, axis, low_vel, high_vel, tacc, tdec)
    def set_home_position_unit(self, connect_no, axis, enable,position):#设置回原点完成后的偏移位置值
        #connect_no:指定链接号
        #axis:指定轴号
        #enable:指定是否使能，0禁止；1先清0，后运动到指定相对位置；2先运动到指定相对位置，在清0
        #position:设置回原点位置
        return self.smc_dll.smc_set_home_position_unit(connect_no, axis,enable, position)
    def set_homemode(self, connect_no, axis, home_dir, vel_mode,  mode,source):#设置回原点方式
        #connect_no:指定链接号
        #axis:指定轴号
        #home_dir:指定回原点方向，0负向，1正向
        #vel:指定回原点速度模式，默认1
        #acc:指定回原点加速度模式，默认1
        #mode:指定回原点方式，0一次回零；
        #source:指定回零计数源，0指令位置计数器，1编码器计数器
        return self.smc_dll.smc_set_homemode(connect_no, axis, home_dir, vel_mode, mode,source)
    def get_homemode(self, connect_no, axis):#获得回原点方式
        #connect_no:指定链接号
        #axis:指定轴号
        #home_dir:返回回原点方向，0反向，1正向
        #vel:返回回原点速度模式，默认1
        #mode:返回回原点方式，0位置回原点，1速度回原点
        #source:返回回零计数源，0指令位置计数器，1编码器计数器
        home_dir = wintypes.WORD()
        vel = ctypes.c_double()
        mode = wintypes.WORD()
        source = wintypes.WORD()
        result = self.smc_dll.smc_get_homemode(connect_no, axis, ctypes.byref(home_dir), ctypes.byref(vel), ctypes.byref(mode), ctypes.byref(source))
        # 返回结果
        return result, home_dir.value, vel.value, mode.value, source.value

    def home_move(self, connect_no, axis):
        #connect_no:指定链接号
        #axis:指定轴号
        return self.smc_dll.smc_home_move(connect_no, axis)

    ##################各种运动方式
    def ptt_table_unit(self, connect_no, axis, count,ptime,ppos):
        #connect_no:指定链接号
        #axis:指定轴号
        #count:指定数据点个数，每个数据表有100个存储空间，每个数据点占用1个存储空间
        #ptime:指定时间数组，单位s(精度ms)
        #ppos:指定位置数组，单位unit(um)
        ptime_array = (ctypes.c_double * 100)(*ptime)
        ppos_array = (ctypes.c_double * 100)(*ppos)
        result=self.smc_dll.smc_ptt_table_unit(connect_no, axis, count, ptime_array,ppos_array)
        return result #, list(ptime_array),list(ppos_array)
    def pts_table_unit(self, connect_no, axis, count,ptime,ppos,ppercent):##############未完善，要改动
        #connect_no:指定链接号
        #axis:指定轴号
        #count:指定数据点个数，每个数据表有1000个存储空间，每个数据点占用1个存储空间
        #ptime:指定时间数组，单位s(精度ms)
        #ppos:指定位置数组，单位unit(um)
        #ppercent:指定速度百分比数组，范围0-100
        ptime_array = (ctypes.c_double * 1000)(*ptime)
        ppos_array = (ctypes.c_double * 1000)(*ppos)
        ppercent_array = (ctypes.c_double * 1000)(*ppercent)
        result=self.smc_dll.smc_pts_table_unit(connect_no, axis, count, ptime_array,ppos_array,ppercent_array)
        return result
    
    def pvt_move(self,connect_no,axisnum,axislist):
        #connectno:指定连接号
        #axisnum：轴数量
        #轴数列表，数组
        axislist_array = (wintypes.WORD *axisnum)(*axislist)
        return self.smc_dll.smc_pvt_move(connect_no,axisnum,axislist_array)

    def t_pmove_extern_unit(self, card_no, axis, midpos, target_pos, min_vel,max_vel, stop_vel,acc, dec, posi_mode):
        #单轴软着陆功能
        #参数说明：
        #card_no:控制器链接号
        #axis:指定轴号，0-（实际轴数-1）
        #midpos:第一段pmove终点位置，单位um
        #target_pos:第二段终点位置，单位um
        #min_vel:起始速度(Vs)，单位um/s
        #max_vel:最大速度(Vm)，单位um/s
        #stop_vel:停止速度(Ve)，单位um/s
        #acc:加速时间0.001-2~31s,
        #dec:减速时间0.001-2~31s
        #posi_mode:相对模式0，绝对模式1
        return self.smc_dll.smc_t_pmove_extern_unit(card_no, axis, midpos, target_pos, min_vel,max_vel, stop_vel,acc, dec, posi_mode)
    