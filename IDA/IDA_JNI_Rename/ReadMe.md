# IDA JNI

Really cool plugin from `trojancyborg` - used it for a long time but needed up today it for IDA 7.4+.

Originally was at `https://github.com/trojancyborg/IDA_JNI_Rename`

# IDA JNI调用重命名脚本
>#### 使用说明：
>先使用ida打开要分析的程序，等ida自动分析完成，使用ALT+F7，执行本脚本，本脚本会根据jni的调用的偏移值在ida中创建两个枚举类型，然后扫描用户的函数，根据汇编指令自动分析jni调用点，添加注释，如果遇到无法识别的指令，可以在**偏移**上面按m键手动设置。支持F5插件，如果未成功自动识别，请按m手动设置。
>
#### 运行脚本前
```
#.text:00005C0A E1 68       LDR     R1, [R4,#(dword_1626C - 0x16260)]
#.text:00005C0C 9B 69       LDR     R3, [R3,#0x18]
#.text:00005C0E 98 47       BLX     R3
```
#### 运行脚本后
```
#.text:00005C0A E1 68       LDR     R1, [R4,#(dword_1626C - 0x16260)]
#.text:00005C0C 9B 69       LDR     R3, [R3,#jni_FindClass] ; jclass FindClass (JNIEnv*, const char*);
#.text:00005C0E 98 47       BLX     R3
```


