# FastDownward Setup Guide

FastDownward has been cloned into the `downward/` directory. However, building it requires several dependencies.

## Prerequisites for FastDownward Build

### Windows Requirements

To build FastDownward on Windows, you need:

1. **Python 3** (Python 3.6 or later)
   - Usually already installed
   - Verify: `python --version`

2. **CMake** (version 3.16 or later)
   - Download from: https://cmake.org/download/
   - Choose "Windows x64 ZIP" or "Windows x64 Installer"
   - Install and add to PATH

3. **Visual Studio 2017 or later** with C++ support
   - Download from: https://visualstudio.microsoft.com/downloads/
   - During installation, select "Desktop development with C++" workload
   - This installs the MSVC compiler (cl.exe) and NMake
   - OR: Use MinGW + GCC (alternative)

4. **NMake** (usually included with Visual Studio)
   - If using MinGW, use make instead

## Installation Steps

### Option 1: Using Visual Studio (Recommended for Windows)

1. **Install CMake**
   - Download from https://cmake.org/download/
   - During installation, select "Add CMake to the system PATH"

2. **Install Visual Studio Community 2022**
   - Download from https://visualstudio.microsoft.com/downloads/
   - Run installer
   - Choose "Desktop development with C++" workload
   - Complete the installation (this may take 20-30 minutes)

3. **Verify Installation**
   ```powershell
   cmake --version
   cl.exe
   nmake /?
   ```

4. **Build FastDownward**
   ```powershell
   cd downward
   python build.py
   ```
   - First build will take 5-10 minutes
   - Output will be in `downward/builds/release/`

### Option 2: Using MinGW (Alternative)

1. **Install CMake** (same as above)

2. **Install MinGW-w64**
   - Download from: https://www.mingw-w64.org/
   - Extract to a directory without spaces
   - Add to PATH

3. **Build FastDownward**
   ```powershell
   cd downward
   python build.py
   ```

## After Successful Build

Once FastDownward is built:

1. The planner executable will be in: `downward/builds/release/bin/`
2. You can run it directly: `downward/fast-downward.py`

## Example Usage

```bash
# From the project root
python downward/fast-downward.py pddl/domains/domain.pddl pddl/problems/problem.pddl --search "astar(lmcut())"
```

## Troubleshooting

### "Could not find 'cmake' on your PATH"
- CMake is not installed or not in PATH
- Download from https://cmake.org/download/
- During install, select "Add CMake to system PATH"

### "cl.exe not found" or "nmake not found"
- Visual Studio C++ compiler not installed
- Install Visual Studio 2017+ with "Desktop development with C++" workload

### Build fails with compilation errors
- Ensure all dependencies are fully installed
- Try: `python build.py --debug` for more information
- Check FastDownward documentation: `downward/BUILD.md`

## Additional Resources

- FastDownward Documentation: https://fast-downward.org/
- BUILD.md in downward/ directory
- README.md in downward/ directory

---

**Next Steps:**
1. Install CMake
2. Install Visual Studio 2022 Community with C++ support
3. Run: `python downward/fast-downward.py --help`
