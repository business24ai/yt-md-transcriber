
![](https://www.youtube.com/watch?v=-2k1rcRzsLA)

### Video

| Field | Value |
|-------|-------|
| Channel | Fireship |
| Title | This free Chinese AI just crushed OpenAI's $200 o1 model... |
| Published | 2025-01-21 |
| URL | https://www.youtube.com/watch?v=-2k1rcRzsLA |


### Transcription

 Yesterday, China released a state-of-the-art, free-and-open-source chain-of-thought-reasoning model with performance that rivals OpenAI-Zo1, which I'm stupidly paying $200 a month for right now. You see, there's two types of people in the tech world right now. In one camp, we have the pessimists who think that AI is overhyped and plateaued with GPT 3.5. In the other camp, we have the optimists who think we're about to see the emergence of an artificial superintelligence that will propel humanity into Ray Kurzweil's technological singularity. Nobody truly knows where things are going, but one thing to remember is that pessimists sound smart while optimists make money. But sometimes it's hard to be an AI optimist because you need to trust hype jet eyes like Sam Altman and closed AI companies like OpenAI. Well luckily, on the same day that TikTok's ban was removed, China gave the world a gift in return in the form of DeepSeek R1. And in today's video, you'll learn exactly how to use it like a senior prompt engineer. It is January 21st, 2025, and you were watching the code report. Yesterday, the course of history changed forever. I know I'm not talking about the return of the king, but rather the release of DeepSeek, which is an MIT license chain of thought model that you can use freely and commercially to make money in your own applications. This model came out while Sam Altman was busy at Trump's inauguration, which is a perfect time to use this new meme template, where Zuckerberg appears to detect a rack overflow in this artificial binary code owned by Jeff Bezos. He's going to have some explaining to do with his wife, but Sam Altman also reigned on the AI Optimus Parade recently when he said that the AI hype was out of control and no, they have not achieved AGI internally. And that's pretty obvious with how buggy chat GPT is. Like recently, a security researcher figured out how to get chat GPT to DDoS websites for you. All you have to do is provide it with a list of similar URLs that point to the same website, and it will crawl them all in parallel, which is something that no truly intelligent being would do. That being said, the release of O1 a few months ago was another step forward in the AI race. But it didn't take long for open source to catch up, and that's what we have with DeepSeek R1. You can see from its benchmarks, DeepSeek R1 is on par with OpenAI O1, and even exceeds it in some benchmarks like math and software engineering. But let me remind you once again that you should never trust benchmarks. Just recently this company Epic AI, which provides a popular math benchmark, only recently disclosed that they've been funded by OpenAI, which feels a bit like a conflict of interest. I don't care about benchmarks anyway and just go off of vibes, so let's go ahead and try out DeepSeek R1 right now. And they have a web-based UI, but you can also use it in places like Hugging Face or Download it locally with tools like Olamma. And that's what I did for its 7 billion parameter model, which weighs about 4.7 gigabytes. However, if you want to use it in its full glory, it'll take over 400 gigabytes and some pretty heavy duty hardware to run it with 671 billion parameters. But if you want something that's on par with O1 Mini, you'll want to go with 32 billion parameters. Now, one thing that makes DeepSeek different is that it doesn't use any supervised fine tuning. Instead, it uses direct reinforcement learning. But what does that even mean? Well, normally, with supervised fine tuning, you show the model a bunch of examples and explain how to solve them step by step. Then evaluate the answers with another model or a human. But R1 doesn't do that and pulls itself up by its own bootstraps, using direct or pure reinforcement learning. Where you give the model a bunch of examples without showing it the solution first, then it tries a bunch of things on its own, and learns or reinforces itself by eventually finding the right solution, just like a real human with reasoning capabilities. DeepSeek also released a brief paper that describes the reinforcement learning algorithm. It looks complicated, but basically for each problem, the AI tries multiple times to generate answers, which are called outputs. The answers are then grouped together and given a reward score. So the AI learns to adjust its approach for answers with a higher score. That's pretty cool, and we can see the model's actual chain of thought if we go ahead and prompt it here with Olama. When prompting a chain of thought model like R1 or O1, you want to keep the prompt as concise and direct as possible. Because unlike other models like GPT-4, the idea is that it does the thinking on its own. Like if I ask it to solve a math problem, you'll notice that it first shows me all the thinking steps. And then after that thinking process is done, it'll show the actual solution. That's pretty cool, but you might be wondering when to use a chain of thought model instead of a regular, large language model. Well basically, the chain of thought models are much better when it comes to complex problem-solving. Things like advanced math problems, puzzles, or coding problems that require detailed planning. But if you want to build a future with AI, you need to learn it from the ground up. And you can do that today for free thanks to this video sponsor, Brilliant. Their platform provides interactive hands-on lessons that demystify the complexity of deep learning. With just a few minutes of effort each day, you can understand the math and computer science behind the seemingly magic technology. I'd recommend starting with Python, then check out their full how large language models work course if you really want to look under the hood of chat GPT. Try everything Brilliant has to offer for free for 30 days by going to Brilliant.org slash fireship or use the QR code on screen. This has been the code report. Thanks for watching and I will see you in the next one.


### Segments

| Timestamp | Text |
|-----------|------|
| [00:00](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=0) |  Yesterday, China released a state-of-the-art, free-and-open-source chain-of-thought-reasoning |
| [00:04](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=4) |  model with performance that rivals OpenAI-Zo1, which I'm stupidly paying $200 a month |
| [00:09](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=9) |  for right now. |
| [00:10](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=10) |  You see, there's two types of people in the tech world right now. |
| [00:12](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=12) |  In one camp, we have the pessimists who think that AI is overhyped and plateaued with |
| [00:16](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=16) |  GPT 3.5. |
| [00:17](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=17) |  In the other camp, we have the optimists who think we're about to see the emergence of |
| [00:21](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=21) |  an artificial superintelligence that will propel humanity into Ray Kurzweil's technological |
| [00:26](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=26) |  singularity. |
| [00:27](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=27) |  Nobody truly knows where things are going, but one thing to remember is that pessimists |
| [00:30](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=30) |  sound smart while optimists make money. |
| [00:32](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=32) |  But sometimes it's hard to be an AI optimist because you need to trust hype jet eyes like |
| [00:36](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=36) |  Sam Altman and closed AI companies like OpenAI. |
| [00:39](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=39) |  Well luckily, on the same day that TikTok's ban was removed, China gave the world a gift |
| [00:43](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=43) |  in return in the form of DeepSeek R1. |
| [00:45](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=45) |  And in today's video, you'll learn exactly how to use it like a senior prompt engineer. |
| [00:49](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=49) |  It is January 21st, 2025, and you were watching the code report. |
| [00:53](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=53) |  Yesterday, the course of history changed forever. |
| [00:55](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=55) |  I know I'm not talking about the return of the king, but rather the release of DeepSeek, |
| [00:59](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=59) |  which is an MIT license chain of thought model that you can use freely and commercially |
| [01:02](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=62) |  to make money in your own applications. |
| [01:04](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=64) |  This model came out while Sam Altman was busy at Trump's inauguration, which is a perfect |
| [01:08](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=68) |  time to use this new meme template, where Zuckerberg appears to detect a rack overflow |
| [01:12](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=72) |  in this artificial binary code owned by Jeff Bezos. |
| [01:15](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=75) |  He's going to have some explaining to do with his wife, but Sam Altman also reigned on |
| [01:18](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=78) |  the AI Optimus Parade recently when he said that the AI hype was out of control and |
| [01:22](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=82) |  no, they have not achieved AGI internally. |
| [01:25](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=85) |  And that's pretty obvious with how buggy chat GPT is. |
| [01:27](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=87) |  Like recently, a security researcher figured out how to get chat GPT to DDoS websites for |
| [01:32](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=92) |  you. |
| [01:33](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=93) |  All you have to do is provide it with a list of similar URLs that point to the same website, |
| [01:36](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=96) |  and it will crawl them all in parallel, which is something that no truly intelligent |
| [01:39](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=99) |  being would do. |
| [01:40](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=100) |  That being said, the release of O1 a few months ago was another step forward in the AI race. |
| [01:44](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=104) |  But it didn't take long for open source to catch up, and that's what we have with DeepSeek |
| [01:48](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=108) |  R1. |
| [01:49](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=109) |  You can see from its benchmarks, DeepSeek R1 is on par with OpenAI O1, and even exceeds |
| [01:53](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=113) |  it in some benchmarks like math and software engineering. |
| [01:56](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=116) |  But let me remind you once again that you should never trust benchmarks. |
| [01:59](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=119) |  Just recently this company Epic AI, which provides a popular math benchmark, only recently |
| [02:04](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=124) |  disclosed that they've been funded by OpenAI, which feels a bit like a conflict of interest. |
| [02:08](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=128) |  I don't care about benchmarks anyway and just go off of vibes, so let's go ahead and |
| [02:11](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=131) |  try out DeepSeek R1 right now. |
| [02:13](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=133) |  And they have a web-based UI, but you can also use it in places like Hugging Face or |
| [02:17](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=137) |  Download it locally with tools like Olamma. |
| [02:20](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=140) |  And that's what I did for its 7 billion parameter model, which weighs about 4.7 gigabytes. |
| [02:24](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=144) |  However, if you want to use it in its full glory, it'll take over 400 gigabytes and some |
| [02:28](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=148) |  pretty heavy duty hardware to run it with 671 billion parameters. |
| [02:32](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=152) |  But if you want something that's on par with O1 Mini, you'll want to go with 32 billion |
| [02:35](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=155) |  parameters. |
| [02:36](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=156) |  Now, one thing that makes DeepSeek different is that it doesn't use any supervised fine |
| [02:40](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=160) |  tuning. |
| [02:41](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=161) |  Instead, it uses direct reinforcement learning. |
| [02:43](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=163) |  But what does that even mean? |
| [02:44](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=164) |  Well, normally, with supervised fine tuning, you show the model a bunch of examples and |
| [02:48](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=168) |  explain how to solve them step by step. |
| [02:50](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=170) |  Then evaluate the answers with another model or a human. |
| [02:52](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=172) |  But R1 doesn't do that and pulls itself up by its own bootstraps, using direct or pure |
| [02:57](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=177) |  reinforcement learning. |
| [02:58](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=178) |  Where you give the model a bunch of examples without showing it the solution first, then |
| [03:01](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=181) |  it tries a bunch of things on its own, and learns or reinforces itself by eventually finding |
| [03:05](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=185) |  the right solution, just like a real human with reasoning capabilities. |
| [03:09](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=189) |  DeepSeek also released a brief paper that describes the reinforcement learning algorithm. |
| [03:13](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=193) |  It looks complicated, but basically for each problem, the AI tries multiple times to generate |
| [03:17](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=197) |  answers, which are called outputs. |
| [03:19](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=199) |  The answers are then grouped together and given a reward score. |
| [03:22](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=202) |  So the AI learns to adjust its approach for answers with a higher score. |
| [03:25](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=205) |  That's pretty cool, and we can see the model's actual chain of thought if we go ahead and |
| [03:28](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=208) |  prompt it here with Olama. |
| [03:30](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=210) |  When prompting a chain of thought model like R1 or O1, you want to keep the prompt as |
| [03:34](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=214) |  concise and direct as possible. |
| [03:36](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=216) |  Because unlike other models like GPT-4, the idea is that it does the thinking on its own. |
| [03:40](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=220) |  Like if I ask it to solve a math problem, you'll notice that it first shows me all the |
| [03:43](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=223) |  thinking steps. |
| [03:44](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=224) |  And then after that thinking process is done, it'll show the actual solution. |
| [03:48](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=228) |  That's pretty cool, but you might be wondering when to use a chain of thought model instead |
| [03:51](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=231) |  of a regular, large language model. |
| [03:53](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=233) |  Well basically, the chain of thought models are much better when it comes to complex problem-solving. |
| [03:57](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=237) |  Things like advanced math problems, puzzles, or coding problems that require detailed |
| [04:01](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=241) |  planning. |
| [04:02](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=242) |  But if you want to build a future with AI, you need to learn it from the ground up. |
| [04:05](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=245) |  And you can do that today for free thanks to this video sponsor, Brilliant. |
| [04:09](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=249) |  Their platform provides interactive hands-on lessons that demystify the complexity of |
| [04:13](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=253) |  deep learning. |
| [04:14](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=254) |  With just a few minutes of effort each day, you can understand the math and computer science |
| [04:18](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=258) |  behind the seemingly magic technology. |
| [04:21](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=261) |  I'd recommend starting with Python, then check out their full how large language models |
| [04:25](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=265) |  work course if you really want to look under the hood of chat GPT. |
| [04:28](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=268) |  Try everything Brilliant has to offer for free for 30 days by going to Brilliant.org slash |
| [04:33](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=273) |  fireship or use the QR code on screen. |
| [04:36](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=276) |  This has been the code report. |
| [04:37](https://www.youtube.com/watch?v=-2k1rcRzsLA&t=277) |  Thanks for watching and I will see you in the next one. |