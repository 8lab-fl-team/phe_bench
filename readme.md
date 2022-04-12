# `phe.paillier`并行计算测试

使用最基础的方式测试对比单进程与多进程、多线程计算的性能表现。

## TL;DR

`phe.paillier`原生无法利用多核进行计算，使用多进程可以充分利用CPU，朴素的统计来看，可以将加密速度提高（核心数量/2）的倍数。相信使用更高效的多核心方案可以进一步提高。

## 测试结果

- keysize = 2048
- 每个核心计算100次（单线程100*核心数次）

|模式|加密次数|总耗时(秒)|平均单次耗时|测试平台|进程数量|
|-|-|-|-|-|-|
|单线程|700|7.89|0.0112|普通PC(8核心)|1|
|多线程|700|8.30|0.0118|普通PC(8核心)|1|
|多进程|700|2.35|0.00335|普通PC(8核心)|7|
|单线程|3100|41.90|0.0135|多核心服务器(32核心)|1|
|多线程|3100|69.11|0.0223|多核心服务器(32核心)|1|
|多进程|3100|2.889|0.00093|多核心服务器(32核心)|31|

> 0.0135 / 0.00093 = 14.51  
> 0.0112 /0.00335 = 3.343283582089552

### 普通PC(8核心)

```shell
Python Version: 3.8.10.final.0 (64 bit)
Cpuinfo Version: 8.0.0
Vendor ID Raw: GenuineIntel
Hardware Raw: 
Brand Raw: Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz
Hz Advertised Friendly: 1.6000 GHz
Hz Actual Friendly: 1.8000 GHz
Hz Advertised: (1600000000, 0)
Hz Actual: (1800000000, 0)
Arch: X86_64
Bits: 64
Count: 8
Arch String Raw: x86_64
L1 Data Cache Size: 
L1 Instruction Cache Size: 
L2 Cache Size: 65536
L2 Cache Line Size: 256
L2 Cache Associativity: 6
L3 Cache Size: 6291456
Stepping: 10
Model: 142
Family: 6
Processor Type: 
Flags: 3dnowprefetch, abm, acpi, adx, aperfmperf, apic, arat, arch_perfmon, art, avx, avx2, bmi1, bmi2, bts, clflush, clflushopt, cmov, constant_tsc, cpuid, cpuid_fault, cx16, cx8, de, ds_cpl, dtes64, dtherm, dts, epb, ept, ept_ad, erms, est, f16c, flexpriority, flush_l1d, fma, fpu, fsgsbase, fxsr, ht, hwp, hwp_act_window, hwp_epp, hwp_notify, ibpb, ibrs, ida, intel_pt, invpcid, invpcid_single, lahf_lm, lm, mca, mce, md_clear, mmx, monitor, movbe, mpx, msr, mtrr, nonstop_tsc, nopl, nx, osxsave, pae, pat, pbe, pcid, pclmulqdq, pdcm, pdpe1gb, pebs, pge, pln, pni, popcnt, pse, pse36, pti, pts, rdrand, rdrnd, rdseed, rdtscp, rep_good, sdbg, sep, sgx, smap, smep, ss, ssbd, sse, sse2, sse4_1, sse4_2, ssse3, stibp, syscall, tm, tm2, tpr_shadow, tsc, tsc_adjust, tsc_deadline_timer, tscdeadline, vme, vmx, vnmi, vpid, x2apic, xgetbv1, xsave, xsavec, xsaveopt, xsaves, xtopology, xtpr
```

### 多核心服务器(32核心)

```shell
Python Version: 3.8.10.final.0 (64 bit)
Cpuinfo Version: 8.0.0
Vendor ID Raw: GenuineIntel
Hardware Raw: 
Brand Raw: Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz
Hz Advertised Friendly: 2.6000 GHz
Hz Actual Friendly: 1.2000 GHz
Hz Advertised: (2600000000, 0)
Hz Actual: (1200000000, 0)
Arch: X86_64
Bits: 64
Count: 32
Arch String Raw: x86_64
L1 Data Cache Size: 
L1 Instruction Cache Size: 
L2 Cache Size: 65536
L2 Cache Line Size: 256
L2 Cache Associativity: 6
L3 Cache Size: 20971520
Stepping: 7
Model: 45
Family: 6
Processor Type: 
Flags: acpi, aes, aperfmperf, apic, arat, arch_perfmon, avx, bts, clflush, cmov, constant_tsc, cpuid, cx16, cx8, dca, de, ds_cpl, dtes64, dtherm, dts, epb, ept, est, flexpriority, flush_l1d, fpu, fxsr, ht, ibpb, ibrs, ida, lahf_lm, lm, mca, mce, md_clear, mmx, monitor, msr, mtrr, nonstop_tsc, nopl, nx, osxsave, pae, pat, pbe, pcid, pclmulqdq, pdcm, pdpe1gb, pebs, pge, pln, pni, popcnt, pse, pse36, pti, pts, rdtscp, rep_good, sep, smx, ss, ssbd, sse, sse2, sse4_1, sse4_2, ssse3, stibp, syscall, tm, tm2, tpr_shadow, tsc, tsc_deadline_timer, tscdeadline, vme, vmx, vnmi, vpid, x2apic, xsave, xsaveopt, xtopology, xtpr
```
