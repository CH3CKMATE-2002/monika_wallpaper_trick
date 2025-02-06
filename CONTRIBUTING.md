# Contributing to Monika's Wallpaper Trick

Thank you for your interest in contributing! To keep the project clean, maintainable, and fun, please follow these guidelines before submitting a pull request.

---

## 🚀 How to Contribute
1. **Fork the repository** and create a new branch:
   ```sh
   git checkout -b feature-my-update
   ```
2. **Make your changes and test them locally.** Ensure your modification does not break existing functionality.
3. **Follow the coding style** (see "Code Style" below).
4. **Submit a pull request (PR)** and describe your changes clearly.
5. **Wait for review and approval** before merging.

---

## 🔥 Pull Request Rules
- ✅ **Explain your changes** in the PR description.
- ✅ **Follow code structure** and keep the style consistent.
- ✅ **Ensure your PR passes GitHub Actions tests.**
- ✅ **Attach proof of testing (e.g., screenshots, logs) for major changes.**
- ❌ **Do not submit PRs with broken code.**
- ❌ **No spam, low-effort, or joke PRs.**

---

## 🖥️ Desktop Environment (DE) Support Contributions
If you're adding support for a new Linux desktop environment (DE) or MacOS, follow these steps:
1. **Use the existing structure in `wallpaper_utils.py`.**
2. **Follow the Linux/Windows function pattern for get/set wallpaper.**
3. **Ensure dependencies for the new DE are handled correctly.**
4. **Attach proof of testing on a real system (e.g., terminal output, screenshots).**

---

## 🛠️ Code Style Guidelines
- **Indentation:** Use 4 spaces (no tabs!).
- **Imports:** Group and order them properly.
- **Function names:** Use `snake_case`.
- **Comments:** Keep them meaningful and concise.

Example formatting:
```python
import os
import platform

def is_macos():  # You may only capitalize if it is a name.
    return platform.system().lower() == "darwin"
```

---

## 📢 Need Help?
If you have any questions, open an **issue** or discuss in a pull request.

Happy coding! 🎉

