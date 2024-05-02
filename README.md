# Introduction

**SimpleScript is a One-click Google Chrome extension that simplifies webpage text to your reading level, powered by generative AI.**

# Background

According to recent statistics, 54% of the US population reads below a 6th-grade level [[1]](#1). This implies that over half of the population might find it challenging to read and understand an average Wikipedia page, which typically has a 14th-grade reading level [[2]](#2). This issue may be even worse in less literate countries.

The internet, at the literacy level, is not fully accessible to the general public. Fortunately, state-of-the-art generative AI technology excels at summarizing and rewriting text, inspiring us to use this technology to make webpages understandable to everyone, effortlessly.

# Project Goal

Our goal is to leverage the content-curating capabilities of generative AI to help users effortlessly understand most web content. We also aim to offer different reading levels allowing users to select the literacy level they are most comfortable with to adjust the web content.

Additionally, we provide a chat function that lets users interact with the generative AI in the context of the entire webpage. For example, they can request summaries, ask questions about specific sections, and more.

# How We Built It

Our frontend is a Chrome extension created entirely using HTML, CSS and JavaScript. We did not use node as our use POC use case was very simple, however, if our application were to go to production, we would need to use some of the more robust features built into packages in npm. This leads us to the API for Simple Script, which is written entirely in Python. Specifically, we use the FastAPI framework to create an application that would allow us to communicate with it from our extension running in a client's browser over HTTPS. We chose Python as it generally has the best SDKs when it comes to Generative AI. We were looking into creating a document upload and chat with it feature as well, and were planning on using QDrant DB, however, this did not fit in our scope for the POC. 

For our deployment process, the frontend was just loaded into chrome as a dev unloaded extension which is what we used to demo. To fully ship the extension, we would need to pack it and publish it to the Chrome Extension store. Our backend was first put into a docker image, whose container is run on an internal Cloudrun in the Google Cloud Platform. These dockerfiles were stored in GCP's Artifact Registry, allowing us to quickly deploy new revisions when we updated the backend. Finally, we used an API gateway which has permission to invoke our backend Cloudrun to allow only authenticated end users from hitting our API. This would allow us to easily add more robust authentication such as Oauth2 later down the line to only allow us to serve authenticated users with our API. However, we are only using Basic Auth in the demo.

# Challenges

Our biggest challenge for this demo was CORS. Since the API Gateway did not natively support CORS from our server's middleware, we had to manually handle the Options request made by CORS in our API layer. Additionally, webpages constatly ran us into rate limit issues for Gemini due to the sheer amount of content present. Finally, Gemini blocked a lot of educational content despite them being in well-respected resources such as Wikipedia, and we were unable to change the model's default filters as it constantly errored when we tried to lower the filters.  

# Feedbacks

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

---
# References
<a id="1">[1]</a>
Data Source: https://www.thinkimpact.com/literacy-statistics/

<a id="2">[2]</a>
Data Source: https://firstmonday.org/ojs/index.php/fm/article/view/3916/3297#:~:text=URL%3A%20https%3A%2F%2Ffirstmonday,100
