from dearpygui.core import *
from dearpygui.simple import *
from dearpygui.demo import *
import os
import numpy as np
import otherFunction
import sys
import cv2

add_additional_font('Dependencies/ALIBABA-PUHUITI-MEDIUM.OTF', 18, glyph_ranges='chinese_simplified_common')
set_main_window_title("扭体标记script")
set_theme("Cherry")
set_main_window_size(640, 890)

# 帮助文档文本内容
def helpText():
    version = get_dearpygui_version()
    add_text("扭体标记脚本1.0")
    add_text(f"DearpyGUI {version}")
    add_text("Author  :9527")
    add_text("特性说明:")
    add_text("尽管窗口尺寸已做适配，但尽量开启窗口最大化进行接下来的操作，以显示最佳效果", bullet=True)
    add_text("建议创建相关文件夹，将需要标记的文件全部存放在内，并且需要注意最好不要出现中文文件名及路径", bullet=True)
    add_text("后续版本或添加数据分析的相关功能", bullet=True)
    add_text("文件格式是.MP4等vedio格式(注意不是文件夹及图片)", bullet=True)
    add_text("文件名与路径名除扩展名外不要有‘.’号", bullet=True)

# 打开调试窗口
def openWindow(sender, data):
    if does_item_exist("开启调试窗口"):
        pass
    else:
        with window("开启调试窗口", on_close=delete_widgets, width=300):
            add_input_text("输入调试窗口", default_value="Please Input!", width=150)
            add_same_line(spacing=10)
            add_button("确认", callback=sliderCallback)
            add_spacing(count=10)
            add_text("支持开启的调试窗口:")
            add_text("logger", bullet=True)
            add_text("metrics", bullet=True)
            add_text("documentation", bullet=True)

# 标记按钮按下后的回调函数
def tabFrame(sender, data):
    tmpList = get_value("list")
    frameNum = get_value("index")
    if tmpList[frameNum]==0.0:
        tmpList[frameNum] = 1.0
        configure_item("标记该frame##2", label="取消标记", callback=tabFrame)
    else:
        tmpList[frameNum] = 0.0
        configure_item("标记该frame##2", label="标记该frame", callback=tabFrame)
    set_value("list", tmpList)

# 保存标签内容
def saveTable(sender, data):
    tmpData = get_value("list")
    result = otherFunction.saveFrame(tmpData, get_value("vedioPath"))
    delete_item("space1", children_only=True)
    if result:
        add_text("该标记文件已保存,可以打开其他文件标记内容", parent="space1")
    else:
        add_text("标记文件保存失败,可能文件已存在,其他原因请联系管理员", parent="space1", color=(255,0,0))
    close_popup("注意##2")

# 选择文件的路径回调函数
def applyWorkDir(sender, data):
    log_debug(sender)
    log_debug(data)
    directory = data[0]
    fileName = data[1]
    with group("WorkSpace", parent="Main"):
        add_spacing(count=10)
        with managed_columns("twoColumn", 2):
            add_columns(name="Colum1", columns=1)
            add_dummy(width=5)
            add_same_line()
            with child("space1", width=int(get_value("width")/2-20), height=int(get_value("height")-80)):
                add_collapsing_header("picHeader", label="WorkSpace", default_open=True, leaf=True, closable=True)
                add_spacing(count=5)
                add_separator()
                add_spacing(count=5)
                add_child("picSpace", width=int(get_value("width")/2-33), height=int(get_value("width")/2-33))
                vedioPath = f"{directory}\{fileName}"
                set_value("vedioPath", vedioPath)
                img, frameCount = otherFunction.cv2Img(vedioPath, 0, int(get_value("width")/2-35))
                if type(img)==type(False):
                    delete_item("space1")
                    if does_item_exist("注意"):
                        pass
                    else:
                        with window("注意", on_close=delete_widgets):
                            add_text("文件路径错误请重新选择！")
                            add_button("确定##1", callback=lambda: delete_item("注意"))
                else:
                    tmpList = [0]*frameCount
                    add_value("list", tmpList)
                    set_value("list", tmpList)
                    add_drawing("t", width=int(get_value("width")/2-37), height=int(get_value("width")/2-37))
                    add_texture("#tex", img, img.shape[1],img.shape[0], format=mvTEX_RGB_INT)
                    draw_image("t", "#tex", [int((int(get_value("width")/2-37)-img.shape[1])/2),int((int(get_value("width")/2-37)-img.shape[0])/2)], [img.shape[1]+int((int(get_value("width")/2-37)-img.shape[1])/2),img.shape[0]+int((int(get_value("width")/2-37)-img.shape[0])/2)], tag="show##dynamic")
                    end()
                    add_spacing(count=8)
                    add_same_line()
                    add_slider_int("frameIndex", default_value=0, max_value=frameCount-1, width=355, callback=sliderCallback)
                    add_spacing(count=8)
                    add_same_line()
                    add_button("标记该frame##2", tip="将该frame标记为扭体", callback=tabFrame)
                    add_same_line(spacing=10)
                    add_button("Save", tip="标记完所有frame后保存标签内容")
                    with popup("Save", "注意##2", modal=True, mousebutton=mvMouseButton_Left):
                        add_text("是否标记完所有的frame?点击确定保存文件,点击取消继续标记.")
                        add_spacing(count=15)
                        add_dummy(width=133)
                        add_same_line()
                        add_button("确定##2", callback=saveTable)
                        add_same_line(spacing=10)
                        add_button("取消##1", callback=lambda: close_popup("注意##2"))
                    end()
            if type(img)!=type(False):
                add_same_line()
                add_dummy(width=5)
                add_same_line()
                add_columns("new", 1)
                with child("space2", width=int(get_value("width")/2-50), height=int(get_value("height")-80)):
                    add_collapsing_header("dataAna", label="DataAnalysis", default_open=True, leaf=True, closable=True)
                    add_spacing(count=15)
                    with child("data1", width=670, height=370):
                        add_text("该版块尚未开放")
                    add_spacing(count=10)
                    add_separator()
                    add_spacing(count=10)
                    with child("data2", width=670, height=370):
                        add_text("该版块尚未开放")

# 查看logger信息
def sliderCallback(sender, data):
    log_debug(f"Sender is: {sender}")
    # f-Strings：一种改进Python格式字符串的新方法`
    if sender=="确认":
        index = get_value("输入调试窗口")
        if index == "logger":
            show_logger()
        elif index == "documentation":
            show_documentation()
        elif index == "metrics":
            show_metrics()
    else:
        index = get_value(sender)
        set_value("index", index)
    log_debug(f"index is: {index}")
    tmpList = get_value("list")
    frameNum = index
    if tmpList[frameNum]==0.0:
        configure_item("标记该frame##2", label="标记该frame", callback=tabFrame)
    else:
        configure_item("标记该frame##2", label="取消标记", callback=tabFrame)
    img, frameCount = otherFunction.cv2Img(get_value("vedioPath"), index,int(get_value("width")/2-35))
    add_texture("#tex", img, img.shape[1],img.shape[0], format=mvTEX_RGB_INT)
    configure_item("t", width=int(get_value("width")/2-37), height=int(get_value("width")/2-37))
    draw_image("t", "#tex", [int((int(get_value("width")/2-37)-img.shape[1])/2),int((int(get_value("width")/2-37)-img.shape[0])/2)], [img.shape[1]+int((int(get_value("width")/2-37)-img.shape[1])/2),img.shape[0]+int((int(get_value("width")/2-37)-img.shape[0])/2)], tag="show##dynamic")

# 删除对应窗口
def delete_widgets(sender, data):
    delete_item(sender)

# 打开文件夹
def OpenFile(sender, data):
    if does_item_exist("HelpText"):
        delete_item("HelpText")
    if does_item_exist("WorkSpace"):
        delete_item("WorkSpace")
    open_file_dialog(callback=applyWorkDir)

# 打开帮助窗口
def HelpWindow(sender, data):
    if does_item_exist("帮助"):
        pass
    else:
        with window("帮助", on_close=delete_widgets, width=640):
            helpText()

# 打开debug快捷键
def renderCall(sender, data):
    if (is_key_down(mvKey_Control)):
        if (is_key_down(mvKey_D)):
            show_debug()
# 窗口尺寸改变的回调函数
def resizeCall(sender, data):
    set_value("width", get_main_window_size()[0])
    set_value("height", get_main_window_size()[1])
    if does_item_exist("WorkSpace"):
        configure_item("space1", width=int(get_value("width")/2-20), height=int(get_value("height")-80))
        configure_item("space2", width=int(get_value("width")/2-50), height=int(get_value("height")-80))
        configure_item("picSpace", width=int(get_value("width")/2-38), height=int(get_value("width")/2-38))

# 主窗口
with window("Main"):
    add_menu_bar("Main Menu Bar")
    add_menu("File")
    add_menu_item("Open", callback=OpenFile)
    add_menu_item("调试窗口", callback=openWindow)
    end()
    add_menu_item("Help", callback=HelpWindow)
    add_menu_item("Exit", callback=lambda: stop_dearpygui())
    end()
    add_group("HelpText")
    helpText() # 帮助文档文本
    add_spacing(count=5)
    add_value("vedioPath", "/")  # 想要设置值必须先添加值
    add_button("Open File", callback=OpenFile, callback_data="HelpText")
    end()

# 添加的全局变量
add_value("width", get_main_window_size()[0])
add_value("height", get_main_window_size()[1])
add_value("index", 0)
set_render_callback(renderCall)
set_resize_callback(resizeCall)

start_dearpygui(primary_window="Main")
# 加入关键词设置Main为主窗口