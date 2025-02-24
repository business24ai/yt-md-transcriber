
![](https://www.youtube.com/watch?v=sGUjmyfof4Q)

### Video

| Field | Value |
|-------|-------|
| Channel | LangChain |
| Title | Building a fully local "deep researcher" with DeepSeek-R1 |
| Published | 2025-01-22 |
| URL | https://www.youtube.com/watch?v=sGUjmyfof4Q |


### Transcription

 this is Lancho Lanchay. DeepSeek just released our one, which is a new fully open source reasoning model from the DeepSeek Lab. And it comes with a paper that describes their training strategy, which is quite cool because reasoning models represent a new scaling paradigm for LLMs. I have a separate video on this that's also coming out soon that you can check out. So the scaling paradigm over the past few years has been next to a contradiction. We've seen many successful chat models train with this. It's system one type thinking, it's fast and intuitive. We often tell the model how to think, what tricks like how to think, think step by step. And the interaction mode is often chat. Now, reason and models are a bit different. They're trained with a different paradigm, RL on chain of thoughts. We'll talk about that a lot in a bit. It's system two reasoning. Often tell the model what you actually want, not how to think. And the interaction mode is a bit different. It's very good for research or planning in the background style tasks that are less interactive. So the really interesting thing here is that we now know how a state of the art reasoning model is trained. So of course, the current state of the art reasoning models from up in AI, the O series models, our closed source. We don't have detailed information about how training works. But this is a very clear illustration of how they built a state of the art reasoning model that is on part of the O1. And you'll see those results here shortly. But let me actually talk through the training strategies. It's very interesting. So deep cigar one uses a combination of fine tuning and reinforcement learning to produce this reasoning model. And as a few different stages. So the first stage is just fine tuning. They take deep seek V3, which is their very strong base chat model. And they fine tune it on some number of thousands of chain of thought reasoning examples. Now they don't actually tell the specific number of examples from my reading of the paper. But the point is they do a fine tuning phase to build a good starting point for RL. Now the second stage here is reinforcement ruling with this approach, GRPO. So what's going on there? Well, they have a separate paper on this. And I do want to talk about that a little bit. So this RL stage one uses GRPO reinforcement learning. It's from this deep seek math paper. Now here's what's going on. For every training example. Now I do want to note how many training examples they use. They have 104,000 for 1000. Training examples of hard verifiable problems in math and coding. For which you need some degree of reasoning, like you need to produce a reasoning trace, typically to solve them. And there are some definitive solutions that can be verified. Those are the two criteria that matter here. So they have all these samples. Now what they're doing is for every training example, they actually produce 64 samples. 64 different attempts to solve the problem. And they score each one of those with some rule-based reward, like correct or incorrect from math or coding. That's pretty straightforward. Now here's what's kind of interesting. They basically compare every sample to the mean of all samples in this 64 sample batch. So that's kind of what they do. For samples with high or low normalizer reward, relative to the group meme, they increase or drop the probability of the model generating all the tokens in that sequence. So what happens is each token in that output gets a positive or negative gradient update. And here's the intuition. It's basically saying, let's make all the choices that led to this correct or incorrect decision more or less likely. So that's actually what they're doing. And so the punchline here is, why do they do this? They're trying to discover good reasoning patterns. And what happens is this makes the model very strong at reasoning. But it loses some general capacities. For example, they mentioned it had potential language mixing issues. So this is where another interesting trick comes into play. If we look at our diagram here, we're right here. So you've actually used reinforcement learning to get a very strong reasoning model. But it's actually a bit weaker in some other capabilities. So what they do is they take the resulting reasoning traces from that model and filter them to get only high quality ones. So the paper talks about this as rejection sampling. So basically filtering the outputs of that first reinforcement learning phase from a bunch of different things. It's not just correctness, but the point is it results in 600,000 reasoning traces that they can then train further on. So that's really the interesting insight here that you can utilize outputs from the first stage of RL to subsequent stages of your model. And that's exactly what they do. So they do a second stage of fine tuning on the results of that sampling, plus 200,000 additional non-reasoning samples in writing in factual QA to what they scribe as restore the general model capabilities while baking in high quality reasoning. So if you look at the diagram here, what's happening is they are filtering the outputs of that first phase of RL. So remember, this model is a very strong reasoner, but it's weak in some general capabilities. And they're combining some non-reasoning examples in their for writing in QA, and they're fine tuning on all that. And then what they argue is, or they present, they get a model that retains very strong reasoning, but also restores general capabilities. So that's the key point. Then after that, they have a final or second round of reinforcement learning with two different rewards. So previously, we talked about they only used a rule-based reward for reasoning on math and coding style problems. Now they include different rewards for helplessness and harm as well as reasoning. And they use a mix of data that includes all reasoning and general problems to really optimizing for both reasoning and general capabilities. OK, so that's really the second stage of RL. Now a final note, which actually is very exciting, we're going to be actually working with more directly here. They also take that data set that they get from that first phase of RL of 600,000 samples. And they actually do knowledge, they take much smaller open source models and fine tune them on those high quality reasoning traces. And then what they get is a bunch of distilled, smaller, R1 models, pretty cool. And some of them you can actually run your laptop as we'll see right here. So what are the results? So they show a bunch of nice results here, deep-seek R1 versus O1 and some smaller models, O1 mini. Really the punchline is, it's very close to R1 on a bunch of interesting challenges related to coding and math. Now one, in particular, pay attention to the sweet bench verified. It's a very popular benchmark for general software engineering challenges. And it is doing indeed quite well, slightly better than O1, apparently. They also have a bunch of distilled models. So here's the thing that is really quite cool. If you look at their distilled QN14B, you look at the benchmark results. And it is pretty close to O1 mini. You can kind of go across and look and commit yourself of this. But look, it's pretty strong. And 14B can actually run on a lot of people's laptops. For example, I have a 32 gig MacBook Pro. And I can run 14B, as we'll see in a bit. So now let's try playing with it. So I pulled deep-seek 14B from Olamma. So you can see they put it tweet-out recently. They host all these models. Pretty cool. You can try to run them on your own hardware. And I'm in a notebook. So all I need to do is grab Lange and Olamma. I'm going to initialize my model. And what's nice is I'm going to use JSON mode with Olamma to also produce JSON outputs and see how well structured outputs work with this model. So first, let's try a simple question. Was the capital of France? Cool. So you see capital of France at Paris. We'll see something else is interesting. These think tokens, OK? If you go around Olamma and you hunt around for this, there's a lot of people talking about these think tokens. They're harder prompt away. I've tried a bunch. They seem to be kind of an annoying thing. They are absolutely part of the training process. You can look at the paper. You can see that these think tokens are actually included in the training. Now let's try JSON mode. So what's interesting is when you use JSON mode, the think tokens are not present. So there is some post-processing happening on the Olamma side that strips them and you get a JSON object out. So it looks like JSON mode, at least, is working. So that's a good thing. I ask them more involved. Question, give me summary on skilling laws for our own models. And again, you see, wow, this is quite verbose. And you can see this think token emitted first. It's like before. And now you get a much more detailed breakdown of its internal thought process. So let's go right and look at Langsmith just to kind of get a better view of this output. So I'm in my Langsmith project now. I'm going to open up this trace. We can see it took 64 seconds. OK, so that's actually pretty long. But again, I'm really pushing the limits of my hardware, running the 14b model. So that's fine. It's a little bit on me. But I wanted to test O1 mini level performance running locally based on the benchmark. So I just want to kind of play with it. OK, so here's the output. Again, it's quite verbose. You can see the think token here emitted. So it does a lot of thinking prior to responding. And it seems to provide a sane response. But again, this issue of a lot of prethinking being emitted is evidently an issue with these models that may be a problem not depending on your application. You can also programmatically remove that. That's another thing to think about. So let's vibe test it a bit more. This is a repo called OlamaDV researcher. And this is basically an evaluator optimized or workflow for report grinding. So what I'm going to do is I'm going to have an open source LLM running locally via Olama, taken input topic from a user, and generate a search query for it, perform web search, get the results, produce a summary, but then reflect on the summary and regenerative question go back. So this loop is going to look kind of like this. You can see query generation research, summary generation reflection, new query, and so forth. This will continue for some set number of cycles that's configurable. And in the end, I'll get a nice summary with sources. And this can be done with any open source LLM. Now I have a separate video in this that talks about building it from scratch. So I'm not going to kind of build everything again. But I will just test this out using R1. So just some specifics here. I have a MacBook Pro M2 Max 32 gig. I found that the 14 billion distilled deep seek R1 model is about at the edge of what I can run, but still it's fun to try as discussed before. All I need to do to run this is basically just set my tably API key that allows for web search and kick off this command. When you do that, you're going to see LLM server spin up in your browser, and you can actually start interacting with it directly. So you're going to see this in your browser. So this is pretty nice. This is the little environment that I like to use to play with assistance that I create using Minecraft. You can see this shows the overall flow of our assistant here. So it's going to generate a query. Do web search, summarize the results, reflect, and go back. This is a nice test bed, though, for looking at different local models. So what you can do is open up this configurable thing, just paste whatever local model on LLM that you've downloaded and want to test. So in my case, let's test 14b. I'll have it iterate twice. So go to loops. And we can ask any question here. So let's say, give me a report on RL training approaches. So fine. All I like to do is submit. So it's generating our query. And it's using structured output. That's good. So that part of the flow is working as expected. Nice. Now it's using tably to do web research. You can look at the repo to dig into that. And I have a separate video on all this in detail. So now it's summarizing my sources. So this is kind of nice. You see it stream as it goes. You can see those think tokens again. Now in the repo, I added a filter to remove them because I found that they do affect some downstream processing. So I'm going to filter this out when I save it to state in my graph. But you can see how much reasoning and thinking it's doing. So now it's reflecting on my summary. And I've stripped out those thinking tokens during this reflection phase. So this is pretty cool. It finds a knowledge gap. Chainer, it's a follow up question. And now I've done more web research. And I'm summarizing based upon my initial summary and the new web resources that I've retrieved. So now here's my updated summary. So it's thinking it needs to extend the summary. OK. I mean, you know, that may not be a bad thing that it is expressing its kind of process for us to see. I mean, look, it's listening to the property resplendid. You see, I'm going to integrate these points. Good. It's highlighting the new resource that it found. Good. OK. So it's being very expressive about everything needs to do based on the instructions I give it. It's done thinking. And cool. It is updating that summary. So you can see now reinforcing learnings to some field of AI. It's going to reflect again. Go back. We'll try that one more time. And again, it pulled a new paper. It's thinking I need to extend the summary further. I mean, in a way, I kind of like this thinking process because it really explains what it's actually doing and how it's reasoning about it. And you can see it's updating its summary. And it actually looks pretty sane, pretty nice. And it gives us some rich about the global market for RL. So fair and. And it exits. So now we get the final summary. So my assistant will add this little summary thing to the top. And we have our nice written summary here and it'll add the sources. And we can go ahead and look at that in Langsmith as well. We can see everything it did. We can look at the final summary, which is actually right here. So here's the summary. And there's our sources. So basically, my take is the Think Tag thing is kind of annoying. I actually kind of like to see that as a developer. It's annoying to manage if you're actually trying to build an application with this because it emits that to the output. You have to process it out. The 14 billion parameter model is at the edge of what I can run locally on my laptop. Of course, it depends on your hardware. And the summary looks quite nice and comprehensive. And I'll run locally. So it's all for free. So listen, it's pretty cool that you can have these reasoning models now running locally on your laptop. Though obviously we'll get better. This Think Token issue will be resolved, I'm sure in the near future. I encourage you to play with it very much. I find it a lot to be a very nice, easy way to access these models. But there's also some other ways to do it. And I think it's a really nice step forward. And it is really cool that we actually have visibility to how these models are trained. And that this is all open source. So thank you to DeepSeek for releasing this and for a lot of me forgetting this up really quickly. So anyway, I hope this was informative. And thanks.


### Segments

| Timestamp | Text |
|-----------|------|
| [00:00](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=0) |  this is Lancho Lanchay. |
| [00:01](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=1) |  DeepSeek just released our one, |
| [00:03](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=3) |  which is a new fully open source reasoning model |
| [00:05](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=5) |  from the DeepSeek Lab. |
| [00:07](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=7) |  And it comes with a paper that describes |
| [00:09](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=9) |  their training strategy, which is quite cool |
| [00:10](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=10) |  because reasoning models represent |
| [00:12](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=12) |  a new scaling paradigm for LLMs. |
| [00:14](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=14) |  I have a separate video on this that's also coming out soon |
| [00:17](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=17) |  that you can check out. |
| [00:18](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=18) |  So the scaling paradigm over the past few years |
| [00:19](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=19) |  has been next to a contradiction. |
| [00:21](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=21) |  We've seen many successful chat models train with this. |
| [00:23](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=23) |  It's system one type thinking, it's fast and intuitive. |
| [00:27](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=27) |  We often tell the model how to think, |
| [00:29](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=29) |  what tricks like how to think, think step by step. |
| [00:32](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=32) |  And the interaction mode is often chat. |
| [00:34](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=34) |  Now, reason and models are a bit different. |
| [00:35](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=35) |  They're trained with a different paradigm, |
| [00:37](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=37) |  RL on chain of thoughts. |
| [00:39](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=39) |  We'll talk about that a lot in a bit. |
| [00:41](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=41) |  It's system two reasoning. |
| [00:44](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=44) |  Often tell the model what you actually want, |
| [00:46](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=46) |  not how to think. |
| [00:47](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=47) |  And the interaction mode is a bit different. |
| [00:49](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=49) |  It's very good for research or planning |
| [00:51](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=51) |  in the background style tasks that are less interactive. |
| [00:54](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=54) |  So the really interesting thing here is that |
| [00:57](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=57) |  we now know how a state of the art reasoning model is trained. |
| [01:02](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=62) |  So of course, the current state of the art reasoning |
| [01:04](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=64) |  models from up in AI, the O series models, our closed source. |
| [01:07](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=67) |  We don't have detailed information about how training works. |
| [01:11](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=71) |  But this is a very clear illustration |
| [01:13](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=73) |  of how they built a state of the art reasoning model |
| [01:16](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=76) |  that is on part of the O1. |
| [01:18](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=78) |  And you'll see those results here shortly. |
| [01:20](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=80) |  But let me actually talk through the training strategies. |
| [01:21](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=81) |  It's very interesting. |
| [01:22](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=82) |  So deep cigar one uses a combination of fine tuning |
| [01:25](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=85) |  and reinforcement learning to produce this reasoning model. |
| [01:29](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=89) |  And as a few different stages. |
| [01:31](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=91) |  So the first stage is just fine tuning. |
| [01:33](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=93) |  They take deep seek V3, which is their very strong base chat model. |
| [01:39](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=99) |  And they fine tune it on some number of thousands |
| [01:42](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=102) |  of chain of thought reasoning examples. |
| [01:44](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=104) |  Now they don't actually tell the specific number of examples |
| [01:47](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=107) |  from my reading of the paper. |
| [01:48](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=108) |  But the point is they do a fine tuning phase |
| [01:50](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=110) |  to build a good starting point for RL. |
| [01:53](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=113) |  Now the second stage here is reinforcement |
| [01:56](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=116) |  ruling with this approach, GRPO. |
| [01:59](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=119) |  So what's going on there? |
| [02:00](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=120) |  Well, they have a separate paper on this. |
| [02:02](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=122) |  And I do want to talk about that a little bit. |
| [02:04](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=124) |  So this RL stage one uses GRPO reinforcement learning. |
| [02:07](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=127) |  It's from this deep seek math paper. |
| [02:10](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=130) |  Now here's what's going on. |
| [02:11](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=131) |  For every training example. |
| [02:13](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=133) |  Now I do want to note how many training examples they use. |
| [02:16](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=136) |  They have 104,000 for 1000. |
| [02:18](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=138) |  Training examples of hard verifiable problems |
| [02:21](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=141) |  in math and coding. |
| [02:23](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=143) |  For which you need some degree of reasoning, |
| [02:25](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=145) |  like you need to produce a reasoning trace, |
| [02:27](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=147) |  typically to solve them. |
| [02:28](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=148) |  And there are some definitive solutions that can be verified. |
| [02:31](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=151) |  Those are the two criteria that matter here. |
| [02:33](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=153) |  So they have all these samples. |
| [02:35](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=155) |  Now what they're doing is for every training example, |
| [02:38](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=158) |  they actually produce 64 samples. |
| [02:40](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=160) |  64 different attempts to solve the problem. |
| [02:43](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=163) |  And they score each one of those with some rule-based reward, |
| [02:45](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=165) |  like correct or incorrect from math or coding. |
| [02:47](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=167) |  That's pretty straightforward. |
| [02:49](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=169) |  Now here's what's kind of interesting. |
| [02:51](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=171) |  They basically compare every sample |
| [02:53](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=173) |  to the mean of all samples in this 64 sample batch. |
| [02:57](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=177) |  So that's kind of what they do. |
| [02:58](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=178) |  For samples with high or low normalizer reward, |
| [03:03](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=183) |  relative to the group meme, they increase or drop |
| [03:06](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=186) |  the probability of the model generating |
| [03:08](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=188) |  all the tokens in that sequence. |
| [03:11](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=191) |  So what happens is each token in that output |
| [03:13](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=193) |  gets a positive or negative gradient update. |
| [03:16](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=196) |  And here's the intuition. |
| [03:17](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=197) |  It's basically saying, let's make all the choices |
| [03:19](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=199) |  that led to this correct or incorrect decision |
| [03:22](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=202) |  more or less likely. |
| [03:23](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=203) |  So that's actually what they're doing. |
| [03:24](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=204) |  And so the punchline here is, why do they do this? |
| [03:27](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=207) |  They're trying to discover good reasoning patterns. |
| [03:29](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=209) |  And what happens is this makes the model very strong at reasoning. |
| [03:34](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=214) |  But it loses some general capacities. |
| [03:36](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=216) |  For example, they mentioned it |
| [03:37](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=217) |  had potential language mixing issues. |
| [03:39](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=219) |  So this is where another interesting trick comes into play. |
| [03:42](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=222) |  If we look at our diagram here, we're right here. |
| [03:45](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=225) |  So you've actually used reinforcement learning |
| [03:47](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=227) |  to get a very strong reasoning model. |
| [03:49](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=229) |  But it's actually a bit weaker in some other capabilities. |
| [03:52](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=232) |  So what they do is they take the resulting reasoning |
| [03:56](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=236) |  traces from that model and filter them |
| [03:59](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=239) |  to get only high quality ones. |
| [04:02](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=242) |  So the paper talks about this as rejection sampling. |
| [04:05](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=245) |  So basically filtering the outputs |
| [04:06](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=246) |  of that first reinforcement learning phase |
| [04:08](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=248) |  from a bunch of different things. |
| [04:09](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=249) |  It's not just correctness, but the point |
| [04:11](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=251) |  is it results in 600,000 reasoning traces |
| [04:14](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=254) |  that they can then train further on. |
| [04:16](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=256) |  So that's really the interesting insight here |
| [04:19](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=259) |  that you can utilize outputs from the first stage of RL |
| [04:22](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=262) |  to subsequent stages of your model. |
| [04:24](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=264) |  And that's exactly what they do. |
| [04:25](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=265) |  So they do a second stage of fine tuning |
| [04:28](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=268) |  on the results of that sampling, plus 200,000 additional non-reasoning |
| [04:33](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=273) |  samples in writing in factual QA to what they |
| [04:36](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=276) |  scribe as restore the general model capabilities |
| [04:40](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=280) |  while baking in high quality reasoning. |
| [04:43](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=283) |  So if you look at the diagram here, what's happening |
| [04:45](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=285) |  is they are filtering the outputs of that first phase of RL. |
| [04:48](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=288) |  So remember, this model is a very strong reasoner, |
| [04:50](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=290) |  but it's weak in some general capabilities. |
| [04:53](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=293) |  And they're combining some non-reasoning examples |
| [04:56](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=296) |  in their for writing in QA, and they're fine tuning on all that. |
| [05:00](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=300) |  And then what they argue is, or they present, |
| [05:02](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=302) |  they get a model that retains very strong reasoning, |
| [05:05](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=305) |  but also restores general capabilities. |
| [05:08](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=308) |  So that's the key point. |
| [05:10](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=310) |  Then after that, they have a final or second round |
| [05:13](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=313) |  of reinforcement learning with two different rewards. |
| [05:16](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=316) |  So previously, we talked about they only |
| [05:18](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=318) |  used a rule-based reward for reasoning |
| [05:20](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=320) |  on math and coding style problems. |
| [05:23](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=323) |  Now they include different rewards for helplessness |
| [05:26](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=326) |  and harm as well as reasoning. |
| [05:28](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=328) |  And they use a mix of data that includes |
| [05:32](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=332) |  all reasoning and general problems |
| [05:34](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=334) |  to really optimizing for both reasoning |
| [05:37](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=337) |  and general capabilities. |
| [05:39](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=339) |  OK, so that's really the second stage of RL. |
| [05:41](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=341) |  Now a final note, which actually is very exciting, |
| [05:43](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=343) |  we're going to be actually working with more directly here. |
| [05:46](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=346) |  They also take that data set that they get |
| [05:49](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=349) |  from that first phase of RL of 600,000 samples. |
| [05:52](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=352) |  And they actually do knowledge, they take |
| [05:55](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=355) |  much smaller open source models and fine tune them |
| [05:58](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=358) |  on those high quality reasoning traces. |
| [06:01](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=361) |  And then what they get is a bunch of distilled, smaller, |
| [06:04](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=364) |  R1 models, pretty cool. |
| [06:06](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=366) |  And some of them you can actually run your laptop |
| [06:08](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=368) |  as we'll see right here. |
| [06:09](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=369) |  So what are the results? |
| [06:10](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=370) |  So they show a bunch of nice results here, |
| [06:13](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=373) |  deep-seek R1 versus O1 and some smaller models, O1 mini. |
| [06:17](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=377) |  Really the punchline is, it's very close to R1 |
| [06:19](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=379) |  on a bunch of interesting challenges related to coding |
| [06:23](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=383) |  and math. |
| [06:24](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=384) |  Now one, in particular, pay attention |
| [06:26](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=386) |  to the sweet bench verified. |
| [06:27](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=387) |  It's a very popular benchmark for general software |
| [06:29](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=389) |  engineering challenges. |
| [06:31](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=391) |  And it is doing indeed quite well, slightly better |
| [06:34](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=394) |  than O1, apparently. |
| [06:36](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=396) |  They also have a bunch of distilled models. |
| [06:38](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=398) |  So here's the thing that is really quite cool. |
| [06:40](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=400) |  If you look at their distilled QN14B, |
| [06:44](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=404) |  you look at the benchmark results. |
| [06:46](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=406) |  And it is pretty close to O1 mini. |
| [06:48](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=408) |  You can kind of go across and look and commit yourself |
| [06:51](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=411) |  of this. |
| [06:52](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=412) |  But look, it's pretty strong. |
| [06:54](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=414) |  And 14B can actually run on a lot of people's laptops. |
| [06:58](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=418) |  For example, I have a 32 gig MacBook Pro. |
| [07:00](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=420) |  And I can run 14B, as we'll see in a bit. |
| [07:04](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=424) |  So now let's try playing with it. |
| [07:06](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=426) |  So I pulled deep-seek 14B from Olamma. |
| [07:10](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=430) |  So you can see they put it tweet-out recently. |
| [07:12](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=432) |  They host all these models. |
| [07:13](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=433) |  Pretty cool. |
| [07:14](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=434) |  You can try to run them on your own hardware. |
| [07:16](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=436) |  And I'm in a notebook. |
| [07:17](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=437) |  So all I need to do is grab Lange and Olamma. |
| [07:21](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=441) |  I'm going to initialize my model. |
| [07:23](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=443) |  And what's nice is I'm going to use JSON mode with Olamma |
| [07:25](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=445) |  to also produce JSON outputs and see how well structured |
| [07:28](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=448) |  outputs work with this model. |
| [07:30](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=450) |  So first, let's try a simple question. |
| [07:32](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=452) |  Was the capital of France? |
| [07:34](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=454) |  Cool. |
| [07:34](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=454) |  So you see capital of France at Paris. |
| [07:36](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=456) |  We'll see something else is interesting. |
| [07:37](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=457) |  These think tokens, OK? |
| [07:40](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=460) |  If you go around Olamma and you hunt around for this, |
| [07:42](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=462) |  there's a lot of people talking about these think tokens. |
| [07:44](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=464) |  They're harder prompt away. |
| [07:46](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=466) |  I've tried a bunch. |
| [07:47](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=467) |  They seem to be kind of an annoying thing. |
| [07:49](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=469) |  They are absolutely part of the training process. |
| [07:51](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=471) |  You can look at the paper. |
| [07:52](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=472) |  You can see that these think tokens are actually |
| [07:54](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=474) |  included in the training. |
| [07:55](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=475) |  Now let's try JSON mode. |
| [07:56](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=476) |  So what's interesting is when you use JSON mode, |
| [07:58](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=478) |  the think tokens are not present. |
| [08:00](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=480) |  So there is some post-processing happening |
| [08:01](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=481) |  on the Olamma side that strips them |
| [08:03](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=483) |  and you get a JSON object out. |
| [08:04](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=484) |  So it looks like JSON mode, at least, is working. |
| [08:06](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=486) |  So that's a good thing. |
| [08:07](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=487) |  I ask them more involved. |
| [08:08](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=488) |  Question, give me summary on skilling laws for our own models. |
| [08:11](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=491) |  And again, you see, wow, this is quite verbose. |
| [08:14](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=494) |  And you can see this think token emitted first. |
| [08:16](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=496) |  It's like before. |
| [08:17](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=497) |  And now you get a much more detailed breakdown |
| [08:21](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=501) |  of its internal thought process. |
| [08:24](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=504) |  So let's go right and look at Langsmith |
| [08:26](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=506) |  just to kind of get a better view of this output. |
| [08:28](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=508) |  So I'm in my Langsmith project now. |
| [08:30](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=510) |  I'm going to open up this trace. |
| [08:31](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=511) |  We can see it took 64 seconds. |
| [08:34](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=514) |  OK, so that's actually pretty long. |
| [08:35](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=515) |  But again, I'm really pushing the limits of my hardware, |
| [08:38](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=518) |  running the 14b model. |
| [08:39](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=519) |  So that's fine. |
| [08:40](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=520) |  It's a little bit on me. |
| [08:42](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=522) |  But I wanted to test O1 mini level performance running |
| [08:46](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=526) |  locally based on the benchmark. |
| [08:48](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=528) |  So I just want to kind of play with it. |
| [08:50](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=530) |  OK, so here's the output. |
| [08:52](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=532) |  Again, it's quite verbose. |
| [08:53](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=533) |  You can see the think token here emitted. |
| [08:55](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=535) |  So it does a lot of thinking prior to responding. |
| [08:59](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=539) |  And it seems to provide a sane response. |
| [09:01](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=541) |  But again, this issue of a lot of prethinking being emitted |
| [09:05](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=545) |  is evidently an issue with these models that may be a problem |
| [09:10](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=550) |  not depending on your application. |
| [09:11](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=551) |  You can also programmatically remove that. |
| [09:14](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=554) |  That's another thing to think about. |
| [09:15](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=555) |  So let's vibe test it a bit more. |
| [09:17](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=557) |  This is a repo called OlamaDV researcher. |
| [09:19](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=559) |  And this is basically an evaluator optimized |
| [09:21](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=561) |  or workflow for report grinding. |
| [09:23](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=563) |  So what I'm going to do is I'm going to have an open source |
| [09:26](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=566) |  LLM running locally via Olama, taken input |
| [09:30](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=570) |  topic from a user, and generate a search query for it, |
| [09:34](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=574) |  perform web search, get the results, produce a summary, |
| [09:37](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=577) |  but then reflect on the summary and regenerative question |
| [09:41](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=581) |  go back. |
| [09:42](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=582) |  So this loop is going to look kind of like this. |
| [09:44](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=584) |  You can see query generation research, summary generation |
| [09:47](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=587) |  reflection, new query, and so forth. |
| [09:49](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=589) |  This will continue for some set number of cycles |
| [09:52](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=592) |  that's configurable. |
| [09:53](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=593) |  And in the end, I'll get a nice summary with sources. |
| [09:55](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=595) |  And this can be done with any open source LLM. |
| [09:57](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=597) |  Now I have a separate video in this that |
| [09:58](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=598) |  talks about building it from scratch. |
| [10:00](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=600) |  So I'm not going to kind of build everything again. |
| [10:02](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=602) |  But I will just test this out using R1. |
| [10:06](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=606) |  So just some specifics here. |
| [10:07](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=607) |  I have a MacBook Pro M2 Max 32 gig. |
| [10:10](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=610) |  I found that the 14 billion distilled deep seek R1 model |
| [10:14](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=614) |  is about at the edge of what I can run, |
| [10:15](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=615) |  but still it's fun to try as discussed before. |
| [10:18](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=618) |  All I need to do to run this is basically just set |
| [10:20](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=620) |  my tably API key that allows for web search |
| [10:22](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=622) |  and kick off this command. |
| [10:24](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=624) |  When you do that, you're going to see LLM server spin up |
| [10:28](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=628) |  in your browser, and you can actually |
| [10:30](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=630) |  start interacting with it directly. |
| [10:31](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=631) |  So you're going to see this in your browser. |
| [10:33](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=633) |  So this is pretty nice. |
| [10:33](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=633) |  This is the little environment that I like to use |
| [10:35](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=635) |  to play with assistance that I create using Minecraft. |
| [10:38](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=638) |  You can see this shows the overall flow of our assistant |
| [10:41](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=641) |  here. |
| [10:42](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=642) |  So it's going to generate a query. |
| [10:43](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=643) |  Do web search, summarize the results, reflect, |
| [10:45](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=645) |  and go back. |
| [10:46](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=646) |  This is a nice test bed, though, for looking |
| [10:49](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=649) |  at different local models. |
| [10:50](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=650) |  So what you can do is open up this configurable thing, |
| [10:53](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=653) |  just paste whatever local model on LLM |
| [10:55](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=655) |  that you've downloaded and want to test. |
| [10:56](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=656) |  So in my case, let's test 14b. |
| [10:59](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=659) |  I'll have it iterate twice. |
| [11:01](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=661) |  So go to loops. |
| [11:02](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=662) |  And we can ask any question here. |
| [11:04](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=664) |  So let's say, give me a report on RL training approaches. |
| [11:11](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=671) |  So fine. |
| [11:11](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=671) |  All I like to do is submit. |
| [11:13](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=673) |  So it's generating our query. |
| [11:14](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=674) |  And it's using structured output. |
| [11:16](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=676) |  That's good. |
| [11:16](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=676) |  So that part of the flow is working as expected. |
| [11:19](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=679) |  Nice. |
| [11:20](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=680) |  Now it's using tably to do web research. |
| [11:22](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=682) |  You can look at the repo to dig into that. |
| [11:23](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=683) |  And I have a separate video on all this in detail. |
| [11:26](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=686) |  So now it's summarizing my sources. |
| [11:28](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=688) |  So this is kind of nice. |
| [11:29](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=689) |  You see it stream as it goes. |
| [11:31](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=691) |  You can see those think tokens again. |
| [11:32](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=692) |  Now in the repo, I added a filter to remove them |
| [11:38](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=698) |  because I found that they do affect some downstream processing. |
| [11:41](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=701) |  So I'm going to filter this out when I save it to state |
| [11:44](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=704) |  in my graph. |
| [11:44](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=704) |  But you can see how much reasoning and thinking it's doing. |
| [11:48](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=708) |  So now it's reflecting on my summary. |
| [11:49](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=709) |  And I've stripped out those thinking tokens |
| [11:51](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=711) |  during this reflection phase. |
| [11:52](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=712) |  So this is pretty cool. |
| [11:53](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=713) |  It finds a knowledge gap. |
| [11:54](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=714) |  Chainer, it's a follow up question. |
| [11:56](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=716) |  And now I've done more web research. |
| [11:57](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=717) |  And I'm summarizing based upon my initial summary |
| [12:01](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=721) |  and the new web resources that I've retrieved. |
| [12:04](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=724) |  So now here's my updated summary. |
| [12:06](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=726) |  So it's thinking it needs to extend the summary. |
| [12:09](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=729) |  OK. |
| [12:09](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=729) |  I mean, you know, that may not be a bad thing |
| [12:13](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=733) |  that it is expressing its kind of process for us to see. |
| [12:18](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=738) |  I mean, look, it's listening to the property resplendid. |
| [12:20](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=740) |  You see, I'm going to integrate these points. |
| [12:21](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=741) |  Good. |
| [12:23](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=743) |  It's highlighting the new resource that it found. |
| [12:25](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=745) |  Good. |
| [12:26](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=746) |  OK. |
| [12:26](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=746) |  So it's being very expressive about everything |
| [12:28](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=748) |  needs to do based on the instructions I give it. |
| [12:30](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=750) |  It's done thinking. |
| [12:31](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=751) |  And cool. |
| [12:33](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=753) |  It is updating that summary. |
| [12:34](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=754) |  So you can see now reinforcing learnings |
| [12:36](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=756) |  to some field of AI. |
| [12:37](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=757) |  It's going to reflect again. |
| [12:38](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=758) |  Go back. |
| [12:40](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=760) |  We'll try that one more time. |
| [12:41](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=761) |  And again, it pulled a new paper. |
| [12:42](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=762) |  It's thinking I need to extend the summary further. |
| [12:44](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=764) |  I mean, in a way, I kind of like this thinking process |
| [12:47](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=767) |  because it really explains what it's actually doing |
| [12:49](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=769) |  and how it's reasoning about it. |
| [12:50](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=770) |  And you can see it's updating its summary. |
| [12:52](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=772) |  And it actually looks pretty sane, pretty nice. |
| [12:55](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=775) |  And it gives us some rich about the global market for RL. |
| [12:57](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=777) |  So fair and. |
| [12:58](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=778) |  And it exits. |
| [12:59](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=779) |  So now we get the final summary. |
| [13:00](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=780) |  So my assistant will add this little summary thing |
| [13:02](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=782) |  to the top. |
| [13:04](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=784) |  And we have our nice written summary here |
| [13:06](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=786) |  and it'll add the sources. |
| [13:07](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=787) |  And we can go ahead and look at that in Langsmith as well. |
| [13:10](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=790) |  We can see everything it did. |
| [13:11](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=791) |  We can look at the final summary, which is actually right here. |
| [13:13](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=793) |  So here's the summary. |
| [13:14](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=794) |  And there's our sources. |
| [13:16](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=796) |  So basically, my take is the Think Tag thing |
| [13:21](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=801) |  is kind of annoying. |
| [13:22](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=802) |  I actually kind of like to see that as a developer. |
| [13:24](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=804) |  It's annoying to manage if you're actually |
| [13:26](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=806) |  trying to build an application with this |
| [13:27](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=807) |  because it emits that to the output. |
| [13:29](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=809) |  You have to process it out. |
| [13:30](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=810) |  The 14 billion parameter model is at the edge of what |
| [13:33](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=813) |  I can run locally on my laptop. |
| [13:35](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=815) |  Of course, it depends on your hardware. |
| [13:37](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=817) |  And the summary looks quite nice and comprehensive. |
| [13:41](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=821) |  And I'll run locally. |
| [13:43](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=823) |  So it's all for free. |
| [13:44](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=824) |  So listen, it's pretty cool that you |
| [13:46](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=826) |  can have these reasoning models now running locally |
| [13:48](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=828) |  on your laptop. |
| [13:49](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=829) |  Though obviously we'll get better. |
| [13:51](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=831) |  This Think Token issue will be resolved, |
| [13:53](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=833) |  I'm sure in the near future. |
| [13:54](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=834) |  I encourage you to play with it very much. |
| [13:56](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=836) |  I find it a lot to be a very nice, easy way |
| [13:58](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=838) |  to access these models. |
| [13:59](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=839) |  But there's also some other ways to do it. |
| [14:01](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=841) |  And I think it's a really nice step forward. |
| [14:04](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=844) |  And it is really cool that we actually |
| [14:07](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=847) |  have visibility to how these models are trained. |
| [14:09](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=849) |  And that this is all open source. |
| [14:11](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=851) |  So thank you to DeepSeek for releasing this |
| [14:13](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=853) |  and for a lot of me forgetting this up really quickly. |
| [14:16](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=856) |  So anyway, I hope this was informative. |
| [14:18](https://www.youtube.com/watch?v=sGUjmyfof4Q&t=858) |  And thanks. |