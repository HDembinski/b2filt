# b2filt

Output filter for [B2 build](https://boostorg.github.io/build) from the [Boost C++ project](https://www.boost.org).

![](doc/clip1.gif)
![](doc/clip2.gif)

## Install

```shell
pip install b2filt
```

## Usage

Just replace any call to `b2` with `b2filt`. All command line options are forwarded to `b2`.

## Features

- Filters out uninteresting stuff, but shows errors verbatim
- Automatically shows long compilation error messages in pager at end of run
- Works perfectly with `-jN`
- Uses `b2` in your current Boost super project and falls back to `b2` available in PATH
- Displays wall time it took to compile/run everything
