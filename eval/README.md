
# The I GOT YOU Evaluation test

This directory contains the evaluation framework for the `IGotYou-agent`.

## How to Run

To run the evaluations, you first need to install the required dependencies by running `pip install "google.adk[eval]"` and `pip install pytest pytest-asyncio `

Once the dependencies are installed, you can run the evaluation using the command bellow, from the root of the project:

```bash
python -m pytest eval/test_eval.py -v
```

## Test Scenarios

The evaluation is designed to test the `IGotYou_Agent` by running it through a predefined conversation. The test scenario is defined in the `simple_eval.test.json` file.

The current test case is:
*   **Hidden gem in Tulum:** The user asks the agent to find out about potential hidden gems spot in Tulum.
*   **User selects Cenote El Pit for diving:** The user asks the agent to give information about the weather in the next few days and find a sweet spot for diving.
