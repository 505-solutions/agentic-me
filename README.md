# AgenticME


Browser agents are experiencing a surge in popularity due to their ability to bridge the gap between large language models and web functionality. However, current solutions operate in the cloud with no absolute guarantees about users' data and account credentials entrusted to these browser agents (e.g. OperatorAI, Manus.im, Claude Computer Use). Leaving them exposed to potential hacks. 

We are using [browser-use](https://github.com/browser-use/browser-use) with connection to OpenAI to perform agentic tasks (this could in the future be upgraded to a locally running LLM). We use a web interface to schedule and monitor the tasks. The whole system is to be deployed in a TEE (such as Marlin Oyster Enclave).

---
 The [big commit](https://github.com/505-solutions/agentic-me/commit/d198f5862e1c46c7a9aca10da7f434e904fe8b6b) was a template import from this public [repo](https://github.com/browser-use/web-ui) 