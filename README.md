
# Introduction

**SimpleScript is a One-click Google Chrome extension that simplifies webpage text to your reading level, powered by generative AI.**

# Background

According to recent statistics, 54% of the US population reads below a 6th-grade level [[1]](#1). This implies that over half of the population might find it challenging to read and understand an average Wikipedia page, which typically has a 14th-grade reading level [[2]](#2). This issue may be even worse in less literate countries.

The internet, at the literacy level, is not fully accessible to the general public. Fortunately, state-of-the-art generative AI technology excels at summarizing and rewriting text, inspiring us to use this technology to make webpages understandable to everyone, effortlessly.

# Project Goal

Our goal is to leverage the content-curating capabilities of generative AI to help users effortlessly understand most web content. We also aim to offer different reading levels allowing users to select the literacy level they are most comfortable with to adjust the web content.

Additionally, we provide a chat function that lets users interact with the generative AI in the context of the entire webpage. For example, they can request summaries, ask questions about specific sections, and more.

# How We Built It

### Current Implementation

Our frontend consists of a Chrome extension developed with HTML, CSS, and JavaScript. We chose not to incorporate Node.js in this phase as the proof of concept (POC) required only basic functionality. The extension was loaded directly into Chrome as an unpacked extension for demonstration purposes.

On the backend, we utilize the FastAPI framework in Python to facilitate communication between the Chrome extension and our server via HTTPS. This setup is contained within a Docker image, hosted on Google Cloud Platform’s Cloud Run. The Dockerfiles are stored in GCP's Artifact Registry, which simplifies the deployment of new backend revisions. Currently, for demo purposes, we implement Basic Authentication using the API gateway service provided by Google Cloud Platform. 

![alt text](https://github.com/KalaRohit/Google-AI-Hackathon/blob/main/Archdiagram.png)

# Challenges

Our biggest challenge for this demo was handling CORS, as our server's middleware did not natively support it through API Gateway. We had to manually manage the Options requests made by CORS at the API layer. Additionally, we frequently encountered rate limit issues with Gemini due to the extensive content on our webpages. Furthermore, Gemini blocked a significant amount of educational content, even from reputable sources like Wikipedia. Attempts to adjust the model's default filters were unsuccessful, as they consistently resulted in errors whenever we tried to lower the settings.


# Feedbacks for Cloud Services Used

#### API Gateway

We used API gateway to add an authentication layer to our simple script API. Deploying was easy due as the only requirement was the OpenAPI spec file that defined our API routes. However, API gateway does not natively support CORS passthrough, and would require another proxy layer infront of it such as an external load balancer to fully integrate this service in a production envrionment. The solution we had to do was to define an Options route in our API layer to handle CORS on our own, as API gateway would not work with our server middleware natively.

#### Gemini

Gemini has a really good SDK that made interacting and function calling with it easy. However, it had the following drawbacks:
- No system prompt, you had to repeat your instructions with each call if your instructions for each call does not change.
- Categorizing non-harmful content as harmful, i.e. we were summarizing a Wikipedia article about the Big Bang, and some responses were blocked even if there was nothing in the source document that seemed harmful in any way.
- Limited capability for history, sometimes, it would hallucinate that it would not have access to session history, even though the history was being passed into it correctly.

# Future Work

To enhance functionality and user experience, we have several future developments planned for SimpleScript:

- **Document Integration**: We'll enable SimpleScript to not only simplify webpages but also documents like PDFs or Word files.
- **Speed Improvements**: Continuous code optimization will make SimpleScript faster and more efficient.
- **Pre-set Chat Prompts**: We'll add commonly used prompts like 'Summarize this page for me,' reducing the need for manual typing.
- **Responsive Design**: We aim to create a flexible design for SimpleScript, allowing users to adjust its size and position to fit their screen and website layout.
- **Security**: We would need to improve our application security, as our API does not validate any user input currently. We would need to implement a robust layer of validation to ensure safe and fair usage of Generative AI in our application.
- **User Privacy**: We would need to make it so that the user has to toggle the extension or whitelist certain websites that the extension can be used on out of respect for their privacy. 

---
# References
<a id="1">[1]</a>
Data Source: https://www.thinkimpact.com/literacy-statistics/

<a id="2">[2]</a>
Data Source: https://firstmonday.org/ojs/index.php/fm/article/view/3916/3297#:~:text=URL%3A%20https%3A%2F%2Ffirstmonday,100

