#coding=UTF8
# 2014/09/05 11:51 
# by trojancyborg
# ida jni调用自动重命名脚本
#例：
# 
#.text:00005C0A E1 68       LDR     R1, [R4,#(dword_1626C - 0x16260)]
#.text:00005C0C 9B 69       LDR     R3, [R3,#0x18]
#.text:00005C0E 98 47       BLX     R3
#
#.text:00005C0A E1 68       LDR     R1, [R4,#(dword_1626C - 0x16260)]
#.text:00005C0C 9B 69       LDR     R3, [R3,#jni_FindClass] ; jclass FindClass (JNIEnv*, const char*);
#.text:00005C0E 98 47       BLX     R3
#

from idautils import *

#枚举名
Enum_JNI_Name = "JNI_Interface"

#通用寄存器
COMMON_REG = ['R%d' % i for i  in  range(0,13)]

#引用类型-----------------------
#立即数字
OP_Immediate = 5

#EXP: LDR R3,[R3,#0x10]
OP_Base_Index_Displacement = 4

#EXP: LDR R3,[R1,R2]
OP_Base_Index = 3

#-------------------------------



jni_names_list = [
	"jni_GetVersion",
	"jni_DefineClass",
	"jni_FindClass",
	"jni_FromReflectedMethod",
	"jni_FromReflectedField",
	"jni_ToReflectedMethod",
	"jni_GetSuperclass",
	"jni_IsAssignableFrom",
	"jni_ToReflectedField",
	"jni_Throw",
	"jni_ThrowNew",
	"jni_ExceptionOccurred",
	"jni_ExceptionDescribe",
	"jni_ExceptionClear",
	"jni_FatalError",
	"jni_PushLocalFrame",
	"jni_PopLocalFrame",
	"jni_NewGlobalRef",
	"jni_DeleteGlobalRef",
	"jni_DeleteLocalRef",
	"jni_IsSameObject",
	"jni_NewLocalRef",
	"jni_EnsureLocalCapacity",
	"jni_AllocObject",
	"jni_NewObject",
	"jni_NewObjectV",
	"jni_NewObjectA",
	"jni_GetObjectClass",
	"jni_IsInstanceOf",
	"jni_GetMethodID",
	"jni_CallObjectMethod",
	"jni_CallObjectMethodV",
	"jni_CallObjectMethodA",
	"jni_CallBooleanMethod",
	"jni_CallBooleanMethodV",
	"jni_CallBooleanMethodA",
	"jni_CallByteMethod",
	"jni_CallByteMethodV",
	"jni_CallByteMethodA",
	"jni_CallCharMethod",
	"jni_CallCharMethodV",
	"jni_CallCharMethodA",
	"jni_CallShortMethod",
	"jni_CallShortMethodV",
	"jni_CallShortMethodA",
	"jni_CallIntMethod",
	"jni_CallIntMethodV",
	"jni_CallIntMethodA",
	"jni_CallLongMethod",
	"jni_CallLongMethodV",
	"jni_CallLongMethodA",
	"jni_CallFloatMethod",
	"jni_CallFloatMethodV",
	"jni_CallFloatMethodA",
	"jni_CallDoubleMethod",
	"jni_CallDoubleMethodV",
	"jni_CallDoubleMethodA",
	"jni_CallVoidMethod",
	"jni_CallVoidMethodV",
	"jni_CallVoidMethodA",
	"jni_CallNonvirtualObjectMethod",
	"jni_CallNonvirtualObjectMethodV",
	"jni_CallNonvirtualObjectMethodA",
	"jni_CallNonvirtualBooleanMethod",
	"jni_CallNonvirtualBooleanMethodV",
	"jni_CallNonvirtualBooleanMethodA",
	"jni_CallNonvirtualByteMethod",
	"jni_CallNonvirtualByteMethodV",
	"jni_CallNonvirtualByteMethodA",
	"jni_CallNonvirtualCharMethod",
	"jni_CallNonvirtualCharMethodV",
	"jni_CallNonvirtualCharMethodA",
	"jni_CallNonvirtualShortMethod",
	"jni_CallNonvirtualShortMethodV",
	"jni_CallNonvirtualShortMethodA",
	"jni_CallNonvirtualIntMethod",
	"jni_CallNonvirtualIntMethodV",
	"jni_CallNonvirtualIntMethodA",
	"jni_CallNonvirtualLongMethod",
	"jni_CallNonvirtualLongMethodV",
	"jni_CallNonvirtualLongMethodA",
	"jni_CallNonvirtualFloatMethod",
	"jni_CallNonvirtualFloatMethodV",
	"jni_CallNonvirtualFloatMethodA",
	"jni_CallNonvirtualDoubleMethod",
	"jni_CallNonvirtualDoubleMethodV",
	"jni_CallNonvirtualDoubleMethodA",
	"jni_CallNonvirtualVoidMethod",
	"jni_CallNonvirtualVoidMethodV",
	"jni_CallNonvirtualVoidMethodA",
	"jni_GetFieldID",
	"jni_GetObjectField",
	"jni_GetBooleanField",
	"jni_GetByteField",
	"jni_GetCharField",
	"jni_GetShortField",
	"jni_GetIntField",
	"jni_GetLongField",
	"jni_GetFloatField",
	"jni_GetDoubleField",
	"jni_SetObjectField",
	"jni_SetBooleanField",
	"jni_SetByteField",
	"jni_SetCharField",
	"jni_SetShortField",
	"jni_SetIntField",
	"jni_SetLongField",
	"jni_SetFloatField",
	"jni_SetDoubleField",
	"jni_GetStaticMethodID",
	"jni_CallStaticObjectMethod",
	"jni_CallStaticObjectMethodV",
	"jni_CallStaticObjectMethodA",
	"jni_CallStaticBooleanMethod",
	"jni_CallStaticBooleanMethodV",
	"jni_CallStaticBooleanMethodA",
	"jni_CallStaticByteMethod",
	"jni_CallStaticByteMethodV",
	"jni_CallStaticByteMethodA",
	"jni_CallStaticCharMethod",
	"jni_CallStaticCharMethodV",
	"jni_CallStaticCharMethodA",
	"jni_CallStaticShortMethod",
	"jni_CallStaticShortMethodV",
	"jni_CallStaticShortMethodA",
	"jni_CallStaticIntMethod",
	"jni_CallStaticIntMethodV",
	"jni_CallStaticIntMethodA",
	"jni_CallStaticLongMethod",
	"jni_CallStaticLongMethodV",
	"jni_CallStaticLongMethodA",
	"jni_CallStaticFloatMethod",
	"jni_CallStaticFloatMethodV",
	"jni_CallStaticFloatMethodA",
	"jni_CallStaticDoubleMethod",
	"jni_CallStaticDoubleMethodV",
	"jni_CallStaticDoubleMethodA",
	"jni_CallStaticVoidMethod",
	"jni_CallStaticVoidMethodV",
	"jni_CallStaticVoidMethodA",
	"jni_GetStaticFieldID",
	"jni_GetStaticObjectField",
	"jni_GetStaticBooleanField",
	"jni_GetStaticByteField",
	"jni_GetStaticCharField",
	"jni_GetStaticShortField",
	"jni_GetStaticIntField",
	"jni_GetStaticLongField",
	"jni_GetStaticFloatField",
	"jni_GetStaticDoubleField",
	"jni_SetStaticObjectField",
	"jni_SetStaticBooleanField",
	"jni_SetStaticByteField",
	"jni_SetStaticCharField",
	"jni_SetStaticShortField",
	"jni_SetStaticIntField",
	"jni_SetStaticLongField",
	"jni_SetStaticFloatField",
	"jni_SetStaticDoubleField",
	"jni_NewString",
	"jni_GetStringLength",
	"jni_GetStringChars",
	"jni_ReleaseStringChars",
	"jni_NewStringUTF",
	"jni_GetStringUTFLength",
	"jni_GetStringUTFChars",
	"jni_ReleaseStringUTFChars",
	"jni_GetArrayLength",
	"jni_NewObjectArray",
	"jni_GetObjectArrayElement",
	"jni_SetObjectArrayElement",
	"jni_NewBooleanArray",
	"jni_NewByteArray",
	"jni_NewCharArray",
	"jni_NewShortArray",
	"jni_NewIntArray",
	"jni_NewLongArray",
	"jni_NewFloatArray",
	"jni_NewDoubleArray",
	"jni_GetBooleanArrayElements",
	"jni_GetByteArrayElements",
	"jni_GetCharArrayElements",
	"jni_GetShortArrayElements",
	"jni_GetIntArrayElements",
	"jni_GetLongArrayElements",
	"jni_GetFloatArrayElements",
	"jni_GetDoubleArrayElements",
	"jni_ReleaseBooleanArrayElements",
	"jni_ReleaseByteArrayElements",
	"jni_ReleaseCharArrayElements",
	"jni_ReleaseShortArrayElements",
	"jni_ReleaseIntArrayElements",
	"jni_ReleaseLongArrayElements",
	"jni_ReleaseFloatArrayElements",
	"jni_ReleaseDoubleArrayElements",
	"jni_GetBooleanArrayRegion",
	"jni_GetByteArrayRegion",
	"jni_GetCharArrayRegion",
	"jni_GetShortArrayRegion",
	"jni_GetIntArrayRegion",
	"jni_GetLongArrayRegion",
	"jni_GetFloatArrayRegion",
	"jni_GetDoubleArrayRegion",
	"jni_SetBooleanArrayRegion",
	"jni_SetByteArrayRegion",
	"jni_SetCharArrayRegion",
	"jni_SetShortArrayRegion",
	"jni_SetIntArrayRegion",
	"jni_SetLongArrayRegion",
	"jni_SetFloatArrayRegion",
	"jni_SetDoubleArrayRegion",
	"jni_RegisterNatives",
	"jni_UnregisterNatives",
	"jni_MonitorEnter",
	"jni_MonitorExit",
	"jni_GetJavaVM",
	"jni_GetStringRegion",
	"jni_GetStringUTFRegion",
	"jni_GetPrimitiveArrayCritical",
	"jni_ReleasePrimitiveArrayCritical",
	"jni_GetStringCritical",
	"jni_ReleaseStringCritical",
	"jni_NewWeakGlobalRef",
	"jni_DeleteWeakGlobalRef",
	"jni_ExceptionCheck",
	"jni_NewDirectByteBuffer",
	"jni_GetDirectBufferAddress",
	"jni_GetDirectBufferCapacity",
	"jni_GetObjectRefType" ]


JNINativeInterface = [ 
	r"void* reserved0;",
	r"void* reserved1;",
	r"void* reserved2;",
	r"void* reserved3;",
	r"jint GetVersion (JNIEnv *);",
	r"jclass DefineClass (JNIEnv*, const char*, jobject, const jbyte*, jsize);",
	r"jclass FindClass (JNIEnv*, const char*);",
	r"jmethodID FromReflectedMethod (JNIEnv*, jobject);",
	r"jfieldID FromReflectedField (JNIEnv*, jobject);",
	r"jobject ToReflectedMethod (JNIEnv*, jclass, jmethodID, jboolean);",
	r"jclass GetSuperclass (JNIEnv*, jclass);",
	r"jboolean IsAssignableFrom (JNIEnv*, jclass, jclass);",
	r"jobject ToReflectedField (JNIEnv*, jclass, jfieldID, jboolean);",
	r"jint Throw (JNIEnv*, jthrowable);",
	r"jint ThrowNew (JNIEnv *, jclass, const char *);",
	r"jthrowable ExceptionOccurred (JNIEnv*);",
	r"void ExceptionDescribe (JNIEnv*);",
	r"void ExceptionClear (JNIEnv*);",
	r"void FatalError (JNIEnv*, const char*);",
	r"jint PushLocalFrame (JNIEnv*, jint);",
	r"jobject PopLocalFrame (JNIEnv*, jobject);",
	r"jobject NewGlobalRef (JNIEnv*, jobject);",
	r"void DeleteGlobalRef (JNIEnv*, jobject);",
	r"void DeleteLocalRef (JNIEnv*, jobject);",
	r"jboolean IsSameObject (JNIEnv*, jobject, jobject);",
	r"jobject NewLocalRef (JNIEnv*, jobject);",
	r"jint EnsureLocalCapacity (JNIEnv*, jint);",
	r"jobject AllocObject (JNIEnv*, jclass);",
	r"jobject NewObject (JNIEnv*, jclass, jmethodID, ...);",
	r"jobject NewObjectV (JNIEnv*, jclass, jmethodID, va_list);",
	r"jobject NewObjectA (JNIEnv*, jclass, jmethodID, jvalue*);",
	r"jclass GetObjectClass (JNIEnv*, jobject);",
	r"jboolean IsInstanceOf (JNIEnv*, jobject, jclass);",
	r"jmethodID GetMethodID (JNIEnv*, jclass, const char*, const char*);",
	r"jobject CallObjectMethod (JNIEnv*, jobject, jmethodID, ...);",
	r"jobject CallObjectMethodV (JNIEnv*, jobject, jmethodID, va_list);",
	r"jobject CallObjectMethodA (JNIEnv*, jobject, jmethodID, jvalue*);",
	r"jboolean CallBooleanMethod (JNIEnv*, jobject, jmethodID, ...);",
	r"jboolean CallBooleanMethodV (JNIEnv*, jobject, jmethodID, va_list);",
	r"jboolean CallBooleanMethodA (JNIEnv*, jobject, jmethodID, jvalue*);",
	r"jbyte CallByteMethod (JNIEnv*, jobject, jmethodID, ...);",
	r"jbyte CallByteMethodV (JNIEnv*, jobject, jmethodID, va_list);",
	r"jbyte CallByteMethodA (JNIEnv*, jobject, jmethodID, jvalue*);",
	r"jchar CallCharMethod (JNIEnv*, jobject, jmethodID, ...);",
	r"jchar CallCharMethodV (JNIEnv*, jobject, jmethodID, va_list);",
	r"jchar CallCharMethodA (JNIEnv*, jobject, jmethodID, jvalue*);",
	r"jshort CallShortMethod (JNIEnv*, jobject, jmethodID, ...);",
	r"jshort CallShortMethodV (JNIEnv*, jobject, jmethodID, va_list);",
	r"jshort CallShortMethodA (JNIEnv*, jobject, jmethodID, jvalue*);",
	r"jint  CallIntMethod (JNIEnv*, jobject, jmethodID, ...);",
	r"jint  CallIntMethodV (JNIEnv*, jobject, jmethodID, va_list);",
	r"jint  CallIntMethodA (JNIEnv*, jobject, jmethodID, jvalue*);",
	r"jlong CallLongMethod (JNIEnv*, jobject, jmethodID, ...);",
	r"jlong CallLongMethodV (JNIEnv*, jobject, jmethodID, va_list);",
	r"jlong CallLongMethodA (JNIEnv*, jobject, jmethodID, jvalue*);",
	r"jfloat CallFloatMethod (JNIEnv*, jobject, jmethodID, ...) __NDK_FPABI__;",
	r"jfloat CallFloatMethodV (JNIEnv*, jobject, jmethodID, va_list) __NDK_FPABI__;",
	r"jfloat CallFloatMethodA (JNIEnv*, jobject, jmethodID, jvalue*) __NDK_FPABI__;",
	r"jdouble CallDoubleMethod (JNIEnv*, jobject, jmethodID, ...) __NDK_FPABI__;",
	r"jdouble CallDoubleMethodV (JNIEnv*, jobject, jmethodID, va_list) __NDK_FPABI__;",
	r"jdouble CallDoubleMethodA (JNIEnv*, jobject, jmethodID, jvalue*) __NDK_FPABI__;",
	r"void CallVoidMethod (JNIEnv*, jobject, jmethodID, ...);",
	r"void CallVoidMethodV (JNIEnv*, jobject, jmethodID, va_list);",
	r"void CallVoidMethodA (JNIEnv*, jobject, jmethodID, jvalue*);",
	r"jobject CallNonvirtualObjectMethod (JNIEnv*, jobject, jclass, jmethodID, ...);",
	r"jobject CallNonvirtualObjectMethodV (JNIEnv*, jobject, jclass, jmethodID, va_list);",
	r"jobject CallNonvirtualObjectMethodA (JNIEnv*, jobject, jclass, jmethodID, jvalue*);",
	r"jboolean CallNonvirtualBooleanMethod (JNIEnv*, jobject, jclass, jmethodID, ...);",
	r"jboolean CallNonvirtualBooleanMethodV (JNIEnv*, jobject, jclass, jmethodID, va_list);",
	r"jboolean CallNonvirtualBooleanMethodA (JNIEnv*, jobject, jclass, jmethodID, jvalue*);",
	r"jbyte CallNonvirtualByteMethod (JNIEnv*, jobject, jclass, jmethodID, ...);",
	r"jbyte CallNonvirtualByteMethodV (JNIEnv*, jobject, jclass, jmethodID, va_list);",
	r"jbyte CallNonvirtualByteMethodA (JNIEnv*, jobject, jclass, jmethodID, jvalue*);",
	r"jchar CallNonvirtualCharMethod (JNIEnv*, jobject, jclass, jmethodID, ...);",
	r"jchar CallNonvirtualCharMethodV (JNIEnv*, jobject, jclass, jmethodID, va_list);",
	r"jchar CallNonvirtualCharMethodA (JNIEnv*, jobject, jclass, jmethodID, jvalue*);",
	r"jshort CallNonvirtualShortMethod (JNIEnv*, jobject, jclass, jmethodID, ...);",
	r"jshort CallNonvirtualShortMethodV (JNIEnv*, jobject, jclass, jmethodID, va_list);",
	r"jshort CallNonvirtualShortMethodA (JNIEnv*, jobject, jclass, jmethodID, jvalue*);",
	r"jint  CallNonvirtualIntMethod (JNIEnv*, jobject, jclass, jmethodID, ...);",
	r"jint  CallNonvirtualIntMethodV (JNIEnv*, jobject, jclass, jmethodID, va_list);",
	r"jint  CallNonvirtualIntMethodA (JNIEnv*, jobject, jclass, jmethodID, jvalue*);",
	r"jlong CallNonvirtualLongMethod (JNIEnv*, jobject, jclass, jmethodID, ...);",
	r"jlong CallNonvirtualLongMethodV (JNIEnv*, jobject, jclass, jmethodID, va_list);",
	r"jlong CallNonvirtualLongMethodA (JNIEnv*, jobject, jclass, jmethodID, jvalue*);",
	r"jfloat CallNonvirtualFloatMethod (JNIEnv*, jobject, jclass, jmethodID, ...) __NDK_FPABI__;",
	r"jfloat CallNonvirtualFloatMethodV (JNIEnv*, jobject, jclass, jmethodID, va_list) __NDK_FPABI__;",
	r"jfloat CallNonvirtualFloatMethodA (JNIEnv*, jobject, jclass, jmethodID, jvalue*) __NDK_FPABI__;",
	r"jdouble CallNonvirtualDoubleMethod (JNIEnv*, jobject, jclass, jmethodID, ...) __NDK_FPABI__;",
	r"jdouble CallNonvirtualDoubleMethodV (JNIEnv*, jobject, jclass, jmethodID, va_list) __NDK_FPABI__;",
	r"jdouble CallNonvirtualDoubleMethodA (JNIEnv*, jobject, jclass, jmethodID, jvalue*) __NDK_FPABI__;",
	r"void CallNonvirtualVoidMethod (JNIEnv*, jobject, jclass, jmethodID, ...);",
	r"void CallNonvirtualVoidMethodV (JNIEnv*, jobject, jclass, jmethodID, va_list);",
	r"void CallNonvirtualVoidMethodA (JNIEnv*, jobject, jclass, jmethodID, jvalue*);",
	r"jfieldID GetFieldID (JNIEnv*, jclass, const char*, const char*);",
	r"jobject GetObjectField (JNIEnv*, jobject, jfieldID);",
	r"jboolean GetBooleanField (JNIEnv*, jobject, jfieldID);",
	r"jbyte GetByteField (JNIEnv*, jobject, jfieldID);",
	r"jchar GetCharField (JNIEnv*, jobject, jfieldID);",
	r"jshort GetShortField (JNIEnv*, jobject, jfieldID);",
	r"jint GetIntField (JNIEnv*, jobject, jfieldID);",
	r"jlong GetLongField (JNIEnv*, jobject, jfieldID);",
	r"jfloat GetFloatField (JNIEnv*, jobject, jfieldID) __NDK_FPABI__;",
	r"jdouble GetDoubleField (JNIEnv*, jobject, jfieldID) __NDK_FPABI__;",
	r"void SetObjectField (JNIEnv*, jobject, jfieldID, jobject);",
	r"void        SetBooleanField (JNIEnv*, jobject, jfieldID, jboolean);",
	r"void SetByteField (JNIEnv*, jobject, jfieldID, jbyte);",
	r"void SetCharField (JNIEnv*, jobject, jfieldID, jchar);",
	r"void SetShortField (JNIEnv*, jobject, jfieldID, jshort);",
	r"void SetIntField (JNIEnv*, jobject, jfieldID, jint);",
	r"void SetLongField (JNIEnv*, jobject, jfieldID, jlong);",
	r"void SetFloatField (JNIEnv*, jobject, jfieldID, jfloat) __NDK_FPABI__;",
	r"void SetDoubleField (JNIEnv*, jobject, jfieldID, jdouble) __NDK_FPABI__;",
	r"jmethodID GetStaticMethodID (JNIEnv*, jclass, const char*, const char*);",
	r"jobject CallStaticObjectMethod (JNIEnv*, jclass, jmethodID, ...);",
	r"jobject CallStaticObjectMethodV (JNIEnv*, jclass, jmethodID, va_list);",
	r"jobject CallStaticObjectMethodA (JNIEnv*, jclass, jmethodID, jvalue*);",
	r"jboolean CallStaticBooleanMethod (JNIEnv*, jclass, jmethodID, ...);",
	r"jboolean CallStaticBooleanMethodV (JNIEnv*, jclass, jmethodID, va_list);",
	r"jboolean CallStaticBooleanMethodA (JNIEnv*, jclass, jmethodID, jvalue*);",
	r"jbyte CallStaticByteMethod (JNIEnv*, jclass, jmethodID, ...);",
	r"jbyte CallStaticByteMethodV (JNIEnv*, jclass, jmethodID, va_list);",
	r"jbyte CallStaticByteMethodA (JNIEnv*, jclass, jmethodID, jvalue*);",
	r"jchar CallStaticCharMethod (JNIEnv*, jclass, jmethodID, ...);",
	r"jchar CallStaticCharMethodV (JNIEnv*, jclass, jmethodID, va_list);",
	r"jchar CallStaticCharMethodA (JNIEnv*, jclass, jmethodID, jvalue*);",
	r"jshort CallStaticShortMethod (JNIEnv*, jclass, jmethodID, ...);",
	r"jshort CallStaticShortMethodV (JNIEnv*, jclass, jmethodID, va_list);",
	r"jshort CallStaticShortMethodA (JNIEnv*, jclass, jmethodID, jvalue*);",
	r"jint CallStaticIntMethod (JNIEnv*, jclass, jmethodID, ...);",
	r"jint CallStaticIntMethodV (JNIEnv*, jclass, jmethodID, va_list);",
	r"jint CallStaticIntMethodA (JNIEnv*, jclass, jmethodID, jvalue*);",
	r"jlong CallStaticLongMethod (JNIEnv*, jclass, jmethodID, ...);",
	r"jlong CallStaticLongMethodV (JNIEnv*, jclass, jmethodID, va_list);",
	r"jlong CallStaticLongMethodA (JNIEnv*, jclass, jmethodID, jvalue*);",
	r"jfloat CallStaticFloatMethod (JNIEnv*, jclass, jmethodID, ...) __NDK_FPABI__;",
	r"jfloat CallStaticFloatMethodV (JNIEnv*, jclass, jmethodID, va_list) __NDK_FPABI__;",
	r"jfloat CallStaticFloatMethodA (JNIEnv*, jclass, jmethodID, jvalue*) __NDK_FPABI__;",
	r"jdouble CallStaticDoubleMethod (JNIEnv*, jclass, jmethodID, ...) __NDK_FPABI__;",
	r"jdouble CallStaticDoubleMethodV (JNIEnv*, jclass, jmethodID, va_list) __NDK_FPABI__;",
	r"jdouble CallStaticDoubleMethodA (JNIEnv*, jclass, jmethodID, jvalue*) __NDK_FPABI__;",
	r"void CallStaticVoidMethod (JNIEnv*, jclass, jmethodID, ...);",
	r"void CallStaticVoidMethodV (JNIEnv*, jclass, jmethodID, va_list);",
	r"void CallStaticVoidMethodA (JNIEnv*, jclass, jmethodID, jvalue*);",
	r"jfieldID GetStaticFieldID (JNIEnv*, jclass, const char*, const char*);",
	r"jobject GetStaticObjectField (JNIEnv*, jclass, jfieldID);",
	r"jboolean GetStaticBooleanField (JNIEnv*, jclass, jfieldID);",
	r"jbyte GetStaticByteField (JNIEnv*, jclass, jfieldID);",
	r"jchar GetStaticCharField (JNIEnv*, jclass, jfieldID);",
	r"jshort GetStaticShortField (JNIEnv*, jclass, jfieldID);",
	r"jint GetStaticIntField (JNIEnv*, jclass, jfieldID);",
	r"jlong GetStaticLongField (JNIEnv*, jclass, jfieldID);",
	r"jfloat GetStaticFloatField (JNIEnv*, jclass, jfieldID) __NDK_FPABI__;",
	r"jdouble GetStaticDoubleField (JNIEnv*, jclass, jfieldID) __NDK_FPABI__;",
	r"void SetStaticObjectField (JNIEnv*, jclass, jfieldID, jobject);",
	r"void SetStaticBooleanField (JNIEnv*, jclass, jfieldID, jboolean);",
	r"void SetStaticByteField (JNIEnv*, jclass, jfieldID, jbyte);",
	r"void SetStaticCharField (JNIEnv*, jclass, jfieldID, jchar);",
	r"void SetStaticShortField (JNIEnv*, jclass, jfieldID, jshort);",
	r"void SetStaticIntField (JNIEnv*, jclass, jfieldID, jint);",
	r"void SetStaticLongField (JNIEnv*, jclass, jfieldID, jlong);",
	r"void SetStaticFloatField (JNIEnv*, jclass, jfieldID, jfloat) __NDK_FPABI__;",
	r"void SetStaticDoubleField (JNIEnv*, jclass, jfieldID, jdouble) __NDK_FPABI__;",
	r"jstring NewString (JNIEnv*, const jchar*, jsize);",
	r"jsize GetStringLength (JNIEnv*, jstring);",
	r"const jchar* GetStringChars (JNIEnv*, jstring, jboolean*);",
	r"void ReleaseStringChars (JNIEnv*, jstring, const jchar*);",
	r"jstring NewStringUTF (JNIEnv*, const char*);",
	r"jsize GetStringUTFLength (JNIEnv*, jstring);",
	r"const char* GetStringUTFChars (JNIEnv*, jstring, jboolean*);",
	r"void ReleaseStringUTFChars (JNIEnv*, jstring, const char*);",
	r"jsize GetArrayLength (JNIEnv*, jarray);",
	r"jobjectArray NewObjectArray (JNIEnv*, jsize, jclass, jobject);",
	r"jobject GetObjectArrayElement (JNIEnv*, jobjectArray, jsize);",
	r"void SetObjectArrayElement (JNIEnv*, jobjectArray, jsize, jobject);",
	r"jbooleanArray NewBooleanArray (JNIEnv*, jsize);",
	r"jbyteArray NewByteArray (JNIEnv*, jsize);",
	r"jcharArray NewCharArray (JNIEnv*, jsize);",
	r"jshortArray NewShortArray (JNIEnv*, jsize);",
	r"jintArray NewIntArray (JNIEnv*, jsize);",
	r"jlongArray NewLongArray (JNIEnv*, jsize);",
	r"jfloatArray NewFloatArray (JNIEnv*, jsize);",
	r"jdoubleArray NewDoubleArray (JNIEnv*, jsize);",
	r"jboolean* GetBooleanArrayElements (JNIEnv*, jbooleanArray, jboolean*);",
	r"jbyte* GetByteArrayElements (JNIEnv*, jbyteArray, jboolean*);",
	r"jchar* GetCharArrayElements (JNIEnv*, jcharArray, jboolean*);",
	r"jshort* GetShortArrayElements (JNIEnv*, jshortArray, jboolean*);",
	r"jint* GetIntArrayElements (JNIEnv*, jintArray, jboolean*);",
	r"jlong* GetLongArrayElements (JNIEnv*, jlongArray, jboolean*);",
	r"jfloat* GetFloatArrayElements (JNIEnv*, jfloatArray, jboolean*);",
	r"jdouble* GetDoubleArrayElements (JNIEnv*, jdoubleArray, jboolean*);",
	r"void ReleaseBooleanArrayElements (JNIEnv*, jbooleanArray, jboolean*, jint);",
	r"void ReleaseByteArrayElements (JNIEnv*, jbyteArray, jbyte*, jint);",
	r"void ReleaseCharArrayElements (JNIEnv*, jcharArray, jchar*, jint);",
	r"void ReleaseShortArrayElements (JNIEnv*, jshortArray, jshort*, jint);",
	r"void ReleaseIntArrayElements (JNIEnv*, jintArray, jint*, jint);",
	r"void ReleaseLongArrayElements (JNIEnv*, jlongArray, jlong*, jint);",
	r"void ReleaseFloatArrayElements (JNIEnv*, jfloatArray, jfloat*, jint);",
	r"void ReleaseDoubleArrayElements (JNIEnv*, jdoubleArray, jdouble*, jint);",
	r"void GetBooleanArrayRegion (JNIEnv*, jbooleanArray, jsize, jsize, jboolean*);",
	r"void GetByteArrayRegion (JNIEnv*, jbyteArray, jsize, jsize, jbyte*);",
	r"void GetCharArrayRegion (JNIEnv*, jcharArray, jsize, jsize, jchar*);",
	r"void GetShortArrayRegion (JNIEnv*, jshortArray, jsize, jsize, jshort*);",
	r"void GetIntArrayRegion (JNIEnv*, jintArray, jsize, jsize, jint*);",
	r"void GetLongArrayRegion (JNIEnv*, jlongArray, jsize, jsize, jlong*);",
	r"void GetFloatArrayRegion (JNIEnv*, jfloatArray, jsize, jsize, jfloat*);",
	r"void GetDoubleArrayRegion (JNIEnv*, jdoubleArray, jsize, jsize, jdouble*);",
	r"void SetBooleanArrayRegion (JNIEnv*, jbooleanArray, jsize, jsize, const jboolean*);",
	r"void SetByteArrayRegion (JNIEnv*, jbyteArray, jsize, jsize, const jbyte*);",
	r"void SetCharArrayRegion (JNIEnv*, jcharArray, jsize, jsize, const jchar*);",
	r"void SetShortArrayRegion (JNIEnv*, jshortArray, jsize, jsize, const jshort*);",
	r"void SetIntArrayRegion (JNIEnv*, jintArray, jsize, jsize, const jint*);",
	r"void SetLongArrayRegion (JNIEnv*, jlongArray, jsize, jsize, const jlong*);",
	r"void SetFloatArrayRegion (JNIEnv*, jfloatArray, jsize, jsize, const jfloat*);",
	r"void SetDoubleArrayRegion (JNIEnv*, jdoubleArray, jsize, jsize, const jdouble*);",
	r"jint RegisterNatives (JNIEnv*, jclass, const JNINativeMethod*, jint);",
	r"jint UnregisterNatives (JNIEnv*, jclass);",
	r"jint MonitorEnter (JNIEnv*, jobject);",
	r"jint MonitorExit (JNIEnv*, jobject);",
	r"jint GetJavaVM (JNIEnv*, JavaVM**);",
	r"void GetStringRegion (JNIEnv*, jstring, jsize, jsize, jchar*);",
	r"void GetStringUTFRegion (JNIEnv*, jstring, jsize, jsize, char*);",
	r"void* GetPrimitiveArrayCritical (JNIEnv*, jarray, jboolean*);",
	r"void ReleasePrimitiveArrayCritical (JNIEnv*, jarray, void*, jint);",
	r"const jchar* GetStringCritical (JNIEnv*, jstring, jboolean*);",
	r"void ReleaseStringCritical (JNIEnv*, jstring, const jchar*);",
	r"jweak NewWeakGlobalRef (JNIEnv*, jobject);",
	r"void DeleteWeakGlobalRef (JNIEnv*, jweak);",
	r"jboolean ExceptionCheck (JNIEnv*);",
	r"jobject NewDirectByteBuffer (JNIEnv*, void*, jlong);",
	r"void* GetDirectBufferAddress (JNIEnv*, jobject);",
	r"jlong GetDirectBufferCapacity (JNIEnv*, jobject);",
	r"jobjectRefType GetObjectRefType (JNIEnv*, jobject);"]

JNIInvokeInterface  = [
	r'void* reserved0',
	r'void* reserved1',
	r'void* reserved2',
	r'jint (*DestroyJavaVM)(JavaVM*)',
	r'jint (*AttachCurrentThread)(JavaVM*, JNIEnv**, void*)',
	r'jint (*DetachCurrentThread)(JavaVM*)',
	r'jint (*GetEnv)(JavaVM*, void**, jint)',
	r'jint (*AttachCurrentThreadAsDaemon)(JavaVM*, JNIEnv**, void*)']

jni_jvmInterface = ["jni_DestroyJavaVM",
				  "jni_AttachCurrentThread",
				  "jni_DetachCurrentThread",
				  "jni_GetEnv",
				  "jni_AttachCurrentThreadAsDaemon"]


#筛选出用户自己的函数
def isUserFunc(addr):
	functionName = idc.get_name(idc.get_func_attr(addr,FUNCATTR_START), ida_name.GN_VISIBLE)
	if functionName.startswith('_'):
		return False
	return True

#判断寄存器是否被指定的操作码 和 操作码类型修改
def FirstWriteRegOp( addr,reg,op,Optype = None):
	addr = ida_search.find_code(addr,SEARCH_NEXT)
	while (addr != BADADDR):
		#第一个操作数是指定寄存器
		if idc.print_operand(addr,0) == reg:
			#操作码相同
			if idc.print_insn_mnem(addr) == op:
				if Optype == None:
					return addr
				elif Optype == idc.get_operand_type(addr,1):
					return addr
				return 0
			else:
				return 0
		addr = ida_search.find_code(addr,SEARCH_NEXT)
	return 0

#往上回朔，找到第一次操作指定寄存器的地址
def writeRegAddr(addr ,reg):
	addr = ida_search.find_code(addr,SEARCH_NEXT)
	while (addr != BADADDR):
		if idc.print_operand(addr,0) == reg:
			return addr
		addr = ida_search.find_code(addr,SEARCH_NEXT)
	return 0

def setComment(addr,offset):
	if (offset / 4) < len(JNINativeInterface) and (offset / 4) >= 4:
		comment = JNINativeInterface[offset / 4]
		idc.set_cmt(addr, comment, 1)
		print('set comment 0x%x' % addr)

def setEnumAndCom(addr):
	offset = idc.get_operand_value(addr,1)
	if (offset / 4) < len(JNINativeInterface) and (offset / 4) >= 4:
		comment = JNINativeInterface[int(offset / 4)]
		#添加注释
		idc.set_cmt(addr, comment, 1)
		#设为枚举类型
		idc.op_enum(addr,1,enum_jni_id,0)
		print('set comment and enum 0x%x' % addr)

def find_LDR(addr, reg):
	addr = ida_search.find_code(addr,SEARCH_NEXT)
	while (addr != BADADDR):

		#查找指定LDR   LDR REG,[XXXX,XXXX]
		if idc.print_insn_mnem(addr) == 'LDR' and idc.print_operand(addr,0) == reg:
			#print idc.print_operand(addr,1),GetOpType(addr,1)

			#右侧的寄存器列表
			regs = filter(lambda x: x.startswith('R') , idc.print_operand(addr,1)[1:-1].split(','))
			regs = list(regs)
			if len(regs) == 0:
				addr = ida_search.find_code(addr,SEARCH_NEXT)
				continue

			# LDR RX,[RX,#0xXX]
			if idc.get_operand_type(addr,1) == OP_Base_Index_Displacement:
				#可能是通过 Table + offset 调用的
				if FirstWriteRegOp( addr, regs[0],'LDR',OP_Base_Index_Displacement):
					#第一个寄存器可能是基地址 
					setEnumAndCom(addr)
					return
				else:
					# [RX,#0xXX] RX 不确定第一个寄存器来源
					off = idc.get_operand_value(addr, 1)

					if len(regs) == 1:
						#LDR RX,[RY + 0xXX]
						#单个寄存器
						wRegaddr = writeRegAddr(addr,regs[0])
						if idc.print_insn_mnem(wRegaddr) == 'ADD' and  FirstWriteRegOp(wRegaddr, regs[0],'LDR',OP_Base_Index):
							off2 = idc.get_operand_value(wRegaddr, 1)
							offset = off + off2
							if off != 0:
								setComment( addr , offset)
							else:
								setEnumAndCom(wRegaddr)
							return
						print('0x%x  Do not support! 0x04' % addr)
						return 

					elif len(regs) > 1 :
						#LDR RX,[RY+ RZ +0xXX]
						#多个寄存器
						print('0x%x  Do not support! 0x05' % addr)
						return 


					#基地址寄存器可能已经包含偏移
					print('0x%x  Do not support! 0x03' % addr)
					return 


			#EXP: LDR R3,[R1,R2]
			elif idc.get_operand_type(addr,1) == OP_Base_Index: 

				# 第一个寄存器可能是基地址
				if  FirstWriteRegOp( addr, regs[0],'LDR', OP_Base_Index_Displacement) > 0:
					#第二个寄存器是mov指令直接设定的偏移值
					wRegAddr = FirstWriteRegOp( addr ,regs[1],"MOV", OP_Immediate)
					if  wRegAddr > 0:
						setEnumAndCom(wRegAddr)
						return

					wRegAddr = FirstWriteRegOp( addr ,regs[1],"LSL", OP_Immediate)
					if  wRegAddr > 0:
						print('LSL 0x%x' % wRegAddr)
						#setEnumAndCom(wRegAddr)
						return
			else:
				print('0x%x  Do not support! 0x02' % addr)
				print(idc.print_operand(addr,1),idc.get_operand_type(addr,1))
		 

		elif idc.print_operand(addr,0) == reg:
			print('0x%x  Do not support! 0x01' % addr)
			return
		addr = ida_search.find_code(addr,SEARCH_NEXT)


#修改指定地址范围中的JNI调用
def modify_jni_call(start,end):
	addr = end
	while (addr > start):
		#逆向遍历指令
		addr = ida_search.find_code(addr,SEARCH_NEXT)
		#BLX操作
		if idc.print_insn_mnem(addr) == "BLX":
			#左边第一个操作数
			Opnd0 = idc.print_operand(addr,0)
			if Opnd0 in COMMON_REG:
				#print '%x %s %s'% (addr,idc.print_insn_mnem(addr),idc.print_operand(addr,0))
				find_LDR(addr, Opnd0)
		pass

	pass

#列出所有函数
def enum_user_function():
	modified = 0
	addr = idc.get_next_func( 0 )
	while (addr != BADADDR):
		function_start = addr
		function_end = idc.get_func_attr(addr,FUNCATTR_END)
		#过滤出用户的函数
		if isUserFunc(addr):
			#尝试校正
			modify_jni_call(function_start,function_end)

		addr = idc.get_next_func(addr)

def init_enum(enum_name, fields_list , offset ,comments):
	ret_id = idc.add_enum(-1,enum_name,0x1100000);
	synthesis = list()

	#将枚举成员，原型声明合并
	for i in range(len(fields_list)):
		synthesis.append((fields_list[i],comments[i],))

	if ret_id != 0xFFFFFFFF:
		for fun,com in synthesis:
			idc.add_enum_member( ret_id , fun , offset , -1);
			ida_enum.set_enum_member_cmt(idc.get_enum_member(ret_id,offset,0,-1),com ,1);
			offset += 4
	return ret_id

#2014/09/10 10:20 
#获取枚举
enum_jni_id = ida_enum.get_enum(Enum_JNI_Name)

init_enum( 'JNI_JVM_FUNC', jni_jvmInterface, 12,JNIInvokeInterface[3:]) 

if enum_jni_id == 0xFFFFFFFF:
	#不存在，则创建
	print('create enum')
	enum_jni_id = init_enum(Enum_JNI_Name, jni_names_list,0x10,JNINativeInterface[4:])

elif ida_enum.get_enum_size(enum_jni_id) != len(jni_names_list):
	#成员个数不对，重新创建
	print('delete enum %s' % Enum_JNI_Name)
	ida_enum.del_enum(enum_jni_id) 
	enum_jni_id = init_enum(Enum_JNI_Name, jni_names_list,0x10,JNINativeInterface[4:])

else:
	print('enum has been created!')

if (enum_jni_id != 0xFFFFFFFF):
	#遍历用户函数
	enum_user_function()
	print('Set jni name Finish!!!')
else:
	print('Create enum fail!!!')

