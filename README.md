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

- Filters out all the uninteresting stuff, but shows errors verbatim.
- Use the `b2` installed in your current Boost super project and fall back to the `b2` available in the PATH.
- Displays the time it took to compile/run everything.
- Designed to work well with `-jN`.
