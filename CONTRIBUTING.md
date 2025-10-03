# Contributing to Meteor Madness Backend

Thank you for your interest in contributing to the Meteor Madness project!

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
    - Clear title and description
    - Steps to reproduce
    - Expected vs actual behavior
    - System information (OS, Python version, etc.)

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue labeled "enhancement"
3. Provide:
    - Clear use case
    - Expected behavior
    - Possible implementation approach

### Code Contributions

1. **Fork the Repository**

    ```bash
    git clone https://github.com/your-username/meteor-madness-backend.git
    cd meteor-madness-backend
    ```

2. **Create a Branch**

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. **Make Changes**

    - Follow the code style guide
    - Write tests for new features
    - Update documentation

4. **Test Your Changes**

    ```bash
    pytest
    python manage.py check
    ```

5. **Commit Your Changes**

    ```bash
    git add .
    git commit -m "Add feature: description"
    ```

6. **Push and Create Pull Request**
    ```bash
    git push origin feature/your-feature-name
    ```

## Code Style Guide

### Python Code Style

-   Follow PEP 8
-   Use meaningful variable names
-   Add docstrings to functions and classes
-   Keep functions focused and small
-   Use type hints where appropriate

Example:

```python
def calculate_impact_energy(mass_kg: float, velocity_mps: float) -> float:
    """
    Calculate kinetic energy of an impact.

    Args:
        mass_kg: Mass in kilograms
        velocity_mps: Velocity in meters per second

    Returns:
        Energy in joules
    """
    return 0.5 * mass_kg * (velocity_mps ** 2)
```

### Django Best Practices

-   Use class-based views with ViewSets
-   Keep business logic in services, not views
-   Use serializers for validation
-   Write migrations for all model changes
-   Use Django's ORM efficiently

### API Design

-   Follow RESTful conventions
-   Use proper HTTP methods
-   Return appropriate status codes
-   Include pagination for list endpoints
-   Provide clear error messages

## Testing

### Writing Tests

```python
from django.test import TestCase
from neos.models import NEO

class NEOModelTest(TestCase):
    def setUp(self):
        self.neo = NEO.objects.create(
            neo_reference_id="123456",
            name="Test Asteroid",
            absolute_magnitude_h=20.5
        )

    def test_size_category(self):
        self.assertEqual(self.neo.size_category, "Small")
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest neos/tests/test_models.py

# Run with coverage
pytest --cov=.
```

## Documentation

-   Update README.md for major features
-   Add API documentation for new endpoints
-   Include docstrings in code
-   Update CHANGELOG.md

## Commit Messages

Format:

```
type: subject

body (optional)

footer (optional)
```

Types:

-   `feat`: New feature
-   `fix`: Bug fix
-   `docs`: Documentation
-   `style`: Formatting
-   `refactor`: Code restructuring
-   `test`: Adding tests
-   `chore`: Maintenance

Example:

```
feat: Add orbital trajectory calculation

Implements Keplerian element conversion to Cartesian coordinates
for orbital trajectory visualization.

Closes #123
```

## Pull Request Process

1. Update documentation
2. Add tests
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers
6. Address review feedback
7. Squash commits if requested

## Code Review

Reviewers will check:

-   Code quality and style
-   Test coverage
-   Documentation
-   Performance implications
-   Security considerations

## Community Guidelines

-   Be respectful and inclusive
-   Provide constructive feedback
-   Help others learn
-   Focus on the code, not the person
-   Follow the Code of Conduct

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

-   Open an issue for questions
-   Join our community chat
-   Email the maintainers

Thank you for contributing! 🙏
