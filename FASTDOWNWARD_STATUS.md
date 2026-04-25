# FastDownward Installation Status

## Current Status ✓

FastDownward planner has been cloned to `downward/` directory.

**Dependency Check Results:**
- ✓ Python 3 is installed (3.14.4)
- ✗ CMake is NOT installed (REQUIRED)
- ✗ C++ Compiler is NOT installed (REQUIRED - either MSVC or GCC)
- ✗ Build tools are NOT installed (REQUIRED - either NMake or Make)

## What's Needed

To complete FastDownward installation, you need to install:

### Required
1. **CMake 3.16+** - https://cmake.org/download/
   - Download Windows installer
   - Install and add to system PATH
   
2. **C++ Compiler** - Choose ONE option:
   - **Visual Studio 2022 Community** (recommended) - https://visualstudio.microsoft.com/downloads/
     - Install with "Desktop development with C++" workload
   - **MinGW-w64** (alternative) - https://www.mingw-w64.org/

## Next Steps

1. Install CMake
2. Install Visual Studio 2022 Community with C++ support
3. Verify installation by running:
   ```powershell
   python check_fastdownward_dependencies.py
   ```
4. Build FastDownward:
   ```powershell
   cd downward
   python build.py
   ```

## Documentation

See [FASTDOWNWARD_SETUP.md](FASTDOWNWARD_SETUP.md) for detailed installation instructions and troubleshooting.

Run `python check_fastdownward_dependencies.py` to verify all dependencies are installed before building.
