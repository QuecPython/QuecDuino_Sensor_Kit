# QuecDuino 入门级传感器实验套件

### **产品介绍**

这是一款由EG800Z系列QuecDuino开发板与二十余种传感器及执行器深度融合打造的入门级实验套件。

QuecDuino入门级传感器实验套件，是专为初学者、创客及教育领域量身定制的一站式开发平台。它完美继承了Arduino开源硬件的易用基因，并创新性地集成了移远通信（Quectel）领先的蜂窝网络技术，让您的物联网构想摆脱繁琐配置，轻松照进现实。

**产品特点**

- **物联网开发**：不同于传统的 Arduino Uno，本套件内置网络通信能力，让你写的代码可以直接连接互联网，无需依赖电脑或额外的 WiFi 模块。
- **Python 上手零门槛**：利用 Python 语言的简洁性，让初学者能跳过复杂的寄存器配置，直接关注物联网逻辑和业务实现。
- **工业级稳定性**：采用移远通信 (Quectel) 工业级模组，适应 -35℃ 到 85℃ 的宽温工作环境，不仅适合学习，也适合工业原型验证。
- **传感器丰富**：多达数十种传感器外设供用户学习使用，丰富的硬件组合能完美还原真实的物联网开发需求。

> !! 本仓库收录 QuecDuino 入门级传感器实验套件搭配使用的基于 QuecPython 开发平台的实验案例。
>
> 更多关于 QuecPython 平台开发方式，请访问 [QuecPython文档中心](https://developer.quectel.com/doc/quecpython/)

### **案例清单**

| 序号 | 案例模块                                                     |
| ---- | ------------------------------------------------------------ |
| 01   | [LED 灯模块](example/01-LED灯/README.md)                     |
| 02   | [单按键模块](example/02-按键中断/README.md)                  |
| 03   | [RGB 灯珠模块](example/03-全彩LED/README.md)                 |
| 04   | [MIC模块](example/04-麦克风(MIC)/README.md)                  |
| 05   | [蜂鸣器模块](example/05-蜂鸣器模块(buzzer)/README.md)        |
| 06   | [水位监测模块](example/06-水位检测模块/README.md)            |
| 07   | [磁簧开关模块(KY-025)](example/07-磁簧开关(KY-025)/README.md) |
| 08   | [障碍物检测模块(KY-032)](example/08-障碍物检测(KY-032)/README.md) |
| 09   | [迷你磁簧(KY-021)](example/09-迷你磁簧(KY-021)/README.md)    |
| 10   | [光敏电阻模块(KY-018)](example/10-光敏电阻模块(KY-018)/README.md) |
| 11   | [火焰检测模块（KY-026）](example/11-火焰检测(KY-026)/README.md) |
| 12   | [魔术光环模块（KY-027）](example/12-魔术光环模块(KY-027)/README.md) |
| 13   | [倾斜模块（KY-020）](example/13-倾斜开关(KY-020)/README.md)  |
| 14   | [超声波模块(HC-SR04)](example/14-超声波模块(HC-SR04)/README.md) |
| 15   | [人体触碰模块(KY-036)](example/15-人体触碰模块(KY-036)/README.md) |
| 16   | [数码管模块(JY005)](example/16-数码管模块(JY005)/README.md)  |
| 17   | [激光发射模块(KY-008)](example/17-激光发射器(KY-008)/README.md) |
| 18   | [水银开关模块(KY-017)](example/18-水银开关(KY-017)/README.md) |
| 19   | [温湿度传感器(AHT20)](example/19-温湿度传感器(AHT20)/README.md) |
| 20   | [模拟压电陶瓷振动传感器)](example/20 - Simulated Piezoelectric Ceramic Vibration Sensor/README.md) |

# EG800Z Duino 开发板固件烧录&使用指导

##  工具下载

请按照如下链接分别下载固件烧录工具和开发调试工具。

固件烧录工具：[QFlash](https://developer.quectel.com/wp-content/uploads/2024/09/QFlash_V7.4_CN.zip)

开发调试工具：[QPYcom](https://developer.quectel.com/wp-content/uploads/2024/09/QPYcom_V4.1.0.zip)

## 固件烧录指导

### 1. 打开 QFlash 程序，点击“**Load FW Files**” 导入固件文件

> !! 请从本仓库的 firmware 文件夹中，获取 QPY_OCPU_EG800Z_CNLA_FW.zip 并解压。

![](media/1.png)

*图1：固件烧录-加载固件文件*

### 2. 选择烧录文件

选择固件包中的`at_command.hbinpkg`文件，点击确定后自动导入。

![](media/2.png)

*图2：固件烧录-选择要下载的固件文件*

### 3. 设备固件下载模式

使用杜邦线短接 **BOOT** 引脚进入下载模式，打开设备管理器，重启设备，查看“端口 (COM 和 LPT)”中的 Quectel QDLoader Port，记录 COM 通道号。

![](media/3.png)

*图3：固件烧录-记录COM通道号*

### 4. 开始下载固件

在 QFlash 中选择对应 COM 通道，点击“**Start**”开始下载，等待进度条完成并显示“**PASS**”。

![](media/4.png)

*图4：固件烧录-“Start”按钮*

下载进程监控

![](media/5.png)

*图5：固件烧录-单击“Start”按钮后自动开始固件升级*

下载完成

![](media/6.png)

*图6：固件烧录-固件升级成功*

## 使用 QPYCom 工具

> !! REPL全称为**Read-Eval-Print-Loop (交互式解释器)**，可以在REPL中进行 QuecPython 程序的调试，是 QPYCom 工具用于 QuecPython 平台提供的主要的开发调试方式。
>
> !! 访问 QuecPython 快速入门：https://developer.quectel.com/doc/quecpython/Getting_started/zh/index.html
>
> !! 更多 QPYCom 工具使用请访问：https://developer.quectel.com/doc/quecpython/Application_guide/zh/dev-tools/QPYcom/index.html

### 通过 REPL 口调试代码

运行 **QPYcom** 工具后，选择正确的串口（波特率无需指定）并打开，即可开始 Python 命令行交互。

- **Step1：进入交互页面**

进入交互页面首先需要打开USB交互口，注意不同平台交互口名称有差异

打开QPYcom工具，端口选择连接**Quectel USB REPL Port**，选择“交互”界面

- **Step2：打开串口**

点击“打开串口”按钮，在交互界面输入**print(‘hello world’)**，按回车后可以看到执行的结果信息

```none
>>> print('hello world')
hello world
```

![img](https://developer.quectel.com/doc/quecpython/Getting_started/zh/4G/media/readme/hello_world.png)

### 脚本下载运行调试

> !! 本仓库提供的 example 脚本文件，均可以下载至模组usr目录中并执行运行。

如下图所示，直接将本地文件通过拖拽方式下载到模组usr目录下。

![](media/QPYcom_drag.jpg)

脚本下载流程：

- **Step1：打开REPL串口**

首先选择模组的交互口,点击“**打开串口**”按钮

- **Step2：通过工具按钮下载**（可选）

可以通过文件页面右侧上面的 "**+**","**-**" 按钮来上传和删除文件

- **Step3：通过拖拽形式下载**（可选）

也可以通过拖拽的方式将文件页面左侧显示的本地文件直接拖拽到右侧模组中去（也可以拖拽文件夹）

- **Step4：下载进度和结果**

下载过程中会在状态栏显示下载文件名和下载进度

- **Step5：运行脚本**

在右侧栏中右键脚本文件，并选择执行即可。