# fork系统调用

**英文名**: fork
**类型**: 系统调用（System Call）
**所属系统**: Linux/Unix
**头文件**: `<unistd.h>`

## 概述

fork是Linux/Unix系统中用于创建新进程的系统调用，是进程管理的核心基础。根据[不懂 fork 与 写时复制，别再说你懂 Linux 内核了](../sources/不懂 fork 与 写时复制，别再说你懂 Linux 内核了.md)的论述，理解fork及其底层的写时复制机制，是区分"了解Linux"与"懂Linux内核"的关键分水岭。

## 函数原型

```c
#include <unistd.h>

pid_t fork(void);
```

## 核心特性

### "调用一次，返回两次"
fork最核心的特性是调用一次但在父进程和子进程中各返回一次。

### 返回值含义

| 返回值 | 含义 | 上下文 |
|--------|------|--------|
| `< 0` | fork失败 | 父进程 |
| `= 0` | 子进程 | 子进程 |
| `> 0` | 子进程PID | 父进程 |

## 基本用法示例

```c
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
    pid_t pid;
    
    // 调用fork创建子进程
    pid = fork();
    
    // 判断fork返回值
    if (pid < 0) {
        // fork失败
        perror("fork error");
        exit(EXIT_FAILURE);
    } else if (pid == 0) {
        // 子进程执行的代码
        printf("I am the child process, my pid is %d, my parent's pid is %d\n", 
               getpid(), getppid());
    } else {
        // 父进程执行的代码
        printf("I am the parent process, my pid is %d, and my child's pid is %d\n", 
               getpid(), pid);
    }
    
    return 0;
}
```

## 进程创建过程

### 1. fork调用前
- 只有一个父进程在运行
- 父进程有自己的地址空间、打开的文件等

### 2. fork调用后
- **创建子进程**: 系统创建新的进程控制块（PCB）
- **资源复制**: 传统方式会复制整个地址空间
- **COW机制**: 现代Linux使用写时复制，共享物理内存页
- **独立执行**: 父子进程从fork后的指令开始并发执行

### 3. 进程关系
- **PID不同**: 父子进程有独立的进程ID
- **PPID关系**: 子进程的父进程ID是父进程的PID
- **资源继承**: 子进程继承父进程的打开文件、环境变量等

## 与写时复制的关系

fork的高效实现依赖于写时复制（COW）技术：

### 传统方式（已被淘汰）
- 立即复制父进程整个地址空间
- 消耗大量内存和时间
- 1GB父进程 → 立即分配1GB给子进程

### COW方式
- **初始阶段**: 父子进程共享物理内存页
- **只读标记**: 共享页被标记为只读
- **延迟复制**: 只有写操作时才复制内存页
- **按需复制**: 只复制被修改的页

详见[[写时复制]]

## 应用场景

### 1. 网络服务器
```c
// 主进程监听，fork子进程处理请求
while (1) {
    accept_connection();
    pid = fork();
    if (pid == 0) {
        handle_request();  // 子进程处理请求
        exit(0);
    }
}
```

### 2. 守护进程创建
```c
// 第一次fork：创建子进程
pid = fork();
if (pid > 0) exit(0);  // 父进程退出

// 第二次fork：确保进程不是会话首进程
pid = fork();
if (pid > 0) exit(0);
```

### 3. 并行处理
```c
// 创建多个子进程并行处理数据
for (int i = 0; i < n; i++) {
    pid = fork();
    if (pid == 0) {
        process_data(i);
        exit(0);
    }
}
// 父进程等待所有子进程
while (wait() > 0);
```

## 常见相关问题

### fork失败的原因
1. **系统进程数达到上限**
2. **内存不足**
3. **用户进程数限制**（ulimit -u）

### fork与exec的区别
- **fork**: 创建子进程，复制父进程地址空间
- **exec**: 替换当前进程的地址空间，加载新程序
- **常见组合**: fork + exec（先fork再exec子进程中运行新程序）

### 僵尸进程与孤儿进程
- **僵尸进程**: 子进程结束，父进程未wait，进程描述符未释放
- **孤儿进程**: 父进程先结束，子进程被init进程（PID 1）收养

## 性能考量

### 内存开销
- **COW前**: 双倍内存占用
- **COW后**: 仅在修改时增加内存
- **实际场景**: 大多数子进程只读不写，内存占用极小

### 创建速度
- **COW前**: 复制1GB内存需要时间
- **COW后**: 几乎瞬间完成（仅需创建PCB和页表）

## 相关系统调用

- **vfork**: 共享地址空间，父进程阻塞
- **clone**: 更精细控制共享内容
- **exec系列**: execve, execvp, execlp等
- **wait/waitpid**: 等待子进程结束

## 相关概念

- [[写时复制]]
- [[进程管理]]
- [[内存管理]]
- [[守护进程]]
- [[缺页异常]]

## 相关实体

- [[Linux内核]]
