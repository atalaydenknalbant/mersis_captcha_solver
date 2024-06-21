# Mersis Captcha Solver

This project automates the process of solving math based captchas on the Mersis website.

## Overview

The Mersis Captcha Solver leverages a pre-trained OCR model (`microsoft/trocr-base-printed`) to recognize text in captcha images, processes the images to enhance legibility, and then uses the recognized text to solve the captcha. The solution integrates with the Mersis website, navigating the site and solving captchas to access specific information.

## Project Structure

- `MathCaptchaSolver.py`: Contains the `CaptchaSolver` class which processes and solves the captcha images.
- `mersis.py`: Main script that uses Selenium to interact with the Mersis website, capture captcha images, and solve them using `CaptchaSolver`.
- `test_captcha_solver.py`: Unit tests for the `CaptchaSolver` class to ensure it solves captchas correctly.
- `requirements.txt`: Lists all Python dependencies required to run the project.
- `.gitignore`: Specifies files and directories to be ignored by git.
- `LICENSE`: Contains the licensing information for the project.
- `captcha.png`: Example captcha image used for testing.

## Installation

To run this project, you'll need Python 3.x and the necessary dependencies. Follow the steps below to set up your environment:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/mersis-captcha-solver.git
    cd mersis-captcha-solver
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the solver**:
    ```sh
    python mersis.py
    ```

## Usage

The `mersis.py` script is the main entry point. It uses Selenium to navigate the Mersis website, fetches captcha images, and uses the `CaptchaSolver` class to solve them. The solution is then entered back into the website to bypass the captcha.

## Captcha Solver

The `CaptchaSolver` class in `MathCaptchaSolver.py` works as follows:

1. **Initialize the solver**:
    ```python
    solver = CaptchaSolver(captcha_image_np)
    ```

2. **Solve the captcha**:
    ```python
    result = solver.solve_captcha()
    ```

## Testing

Unit tests for the captcha solver can be found in `test_captcha_solver.py`. To run the tests, use:

```sh
python -m unittest test_captcha_solver.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements or find bugs.
