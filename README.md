# Job Cloud
> Word clouds for job listings

![Cloud Image](docs/images/engineer-irvine.png)

## Usage
```python

from job_cloud.generator import ImageGenerator

generator = ImageGenerator(
    width=500,
    height=500,
    theme='dusk',
    cloud_font='arial-black',
    text_font='arial-bold',
    padding=40,
    job_title_text='Software Engineer',
    job_location_text='Irvine, CA'
)

cloud_image = generator.generate('foobar.png', description='Foobar job description')

```

See docstrings for specifics

