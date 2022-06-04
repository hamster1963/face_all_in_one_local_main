# 爱萝卜人脸一体机代码
## 文件结构
- [主程序文件](face_client.py)
- [seeta测试文件](seeta动态库测试t.py)
- [子功能测试文件](本地子功能模块测试.py)
- [数据库测试](本地更新人脸测试.py)
## 人脸模型位置
- (/seetaface/)
## Python接口编译
在编译时需要指定编译目标平台，默认为Linux平台，可以通过命令行指定：
cd到seetaface目录下，执行：
- bash编译：
    ```bash
    mkdir build && cd build
    cmake ..
    make
    ```
将在lib文件夹下产生libSeetaFaceAPI.so文件
```bash
sudo echo  ${项目路径}/seetaface/lib/ > /etc/ld.so.conf.d/seetaface6.con  
sudo ldconfig
```
## 动态库测试
- 动态库测试：
    ```bash
    python3 seeta动态库测试t.py
    ```
    
## 全部文件
https://pan.baidu.com/s/15qsbLLOQJxG--Wbs7jIJzg?pwd=b3fk
