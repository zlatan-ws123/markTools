# 内部自用小鼠形态学标记脚本

### 1、安装与运行：

建议使用conda独立环境，可根据requirement文件安装对应包。目前不支持Linux、mac系统。

- 运行：

  到对应工作路径下运行main.py文件

```powershell
python main.py
```



### 2、特性说明：

- GUI使用的[DearPyGui](https://github.com/hoffstadt/DearPyGui)开源框架
- 尽管窗口尺寸已做适配，但尽量开启窗口最大化进行接下来的操作，以显示最佳效果
- 建议创建相关文件夹，将需要标记的文件全部存放在内，并且需要注意最好不要出现中文文件名及路径
- 后续版本或添加数据分析的相关功能
- 文件格式是.MP4等vedio格式(注意不是文件夹及图片
- 文件名与路径名除扩展名外不要有‘.’号
- ctrl+d打开debug窗口