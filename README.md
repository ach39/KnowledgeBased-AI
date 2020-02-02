# Knowledge Based Artificial Intelligence

Design and implementation of an AI agent that can solve 2x2 as well as 3x3 Raven’s Progressive Matrices (RPM).
This six months long projects was developed in three phases, incrementally buidling upon Knowledge-Based AI principles and framework. 


### 1. _Problem-solving approach and design considerations_

Agent uses ‘Classification’ to categorize RPM problems either as 2x2 or 3x3 and then invokes appropriate plan to solve that problem. Each Plan has a rule-set that helps agent determines sequence of transformations to execute to achieve the goal. Agent uses 'Frames' (for knowledge representation) and 'Generate and Test' in conjunction with 'Planning' for problem solving. With help of Pillow (Python Image Processing) library, Agent employs Visuospatial Analogy at its core to solve the problem.

In some cases Pillow APIs are not sufficient to detect the transformation reliably. In such scenarios, Agent converts the image to a numpy array and perform some thresholding before checking for any transformation.

### 2. _Results_   
Agent finished Basic and Challenge questions (96 questions in all) in 2 mins 9secs, with 1.34 secs of average timer per question, achieveing 93% (89/96) accuracy. 
![results](https://github.com/ach39/KnowledgeBased-AI/blob/master/imgs/results.png)


### 3. _Simplified view of Agent’s framework_
![framework](https://github.com/ach39/KnowledgeBased-AI/blob/master/imgs/Agent's%20framework.png)

### 4. _Agent's Answer selection process_
![Answer Selection](https://github.com/ach39/KnowledgeBased-AI/blob/master/imgs/answer_selection.png)
