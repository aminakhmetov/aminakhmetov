### ML-ZoomCamp 2022: Midterm Project

#### General description
We use a data set (https://www.openml.org/search?type=data&sort=runs&status=any&id=40536) to try to predict whether there will be match on a dating service, supposedly run on a website, where users can create profiles, fill out a questionaire about interest, evalute other profiles and then service would make a recommendation, should there be a match between profiles or not. We try to solve a classification problem with prediction of "match" (yes/no) variable.

#### Video-demonstration about running the locally deployed service
[![Demonstration of how to run proposed service](https://img.youtube.com/vi/8UtyuKU3F1w/0.jpg)](https://youtu.be/8UtyuKU3F1w)

#### General Instructions on deployment
1. One can see the Exploratory Data Analysis and training of the model in Midterm Project-Opt.ipynb notebook.
2. One can train model and create a bento service using separate train.py script.
3. One can launch a service using predict.py script, particularly through command: "bentoml serve predict.py:svc --production"
4. One can use file located in files_for_building_bentoml_service folder, that should be copied (as well as predict.py file) to latest bento model folder (~/bentoml/models/dating_service/<latest>) to build a bento "service" using command "bentoml build"
5. One can find servce that was build on "~/bentoml/bentos" or can copy from current repository the folder "dating_app"
6. The if one would like to build a docker image, the dockerfile can be found: "dating_app/env/docker/Dockerfile"

#### Describtion of the dataset
The dataset is from an experiment on speed dating, and was intended for analysis purposes, thus so in order to make realistic application, we have to decide how/if adapt some parameters of a dataset, such as "decision" and "decision_o", i.e. whether each particiapnt made decison match/no_match on the night of the event. These parameters may not be viable parameters of the application. However, due to model precsion problem we would still require some data from portential partner side, some small amount of evaluations of potential partner of a requester of service.

Attribute Information: (from URL above)

 * gender: Gender of self  
 * age: Age of self  
 * age_o: Age of partner  
 * d_age: Difference in age  
 * race: Race of self  
 * race_o: Race of partner  
 * samerace: Whether the two persons have the same race or not.  
 * importance_same_race: How important is it that partner is of same race?  
 * importance_same_religion: How important is it that partner has same religion?  
 * field: Field of study  
 * pref_o_attractive: How important does partner rate attractiveness  
 * pref_o_sinsere: How important does partner rate sincerity  
 * pref_o_intelligence: How important does partner rate intelligence  
 * pref_o_funny: How important does partner rate being funny  
 * pref_o_ambitious: How important does partner rate ambition  
 * pref_o_shared_interests: How important does partner rate having shared interests  
 * attractive_o: Rating by partner (about me) at night of event on attractiveness  
 * sincere_o: Rating by partner (about me) at night of event on sincerity  
 * intelligence_o: Rating by partner (about me) at night of event on intelligence  
 * funny_o: Rating by partner (about me) at night of event on being funny  
 * ambitous_o: Rating by partner (about me) at night of event on being ambitious  
 * shared_interests_o: Rating by partner (about me) at night of event on shared interest  
 * attractive_important: What do you look for in a partner - attractiveness  
 * sincere_important: What do you look for in a partner - sincerity  
 * intellicence_important: What do you look for in a partner - intelligence  
 * funny_important: What do you look for in a partner - being funny  
 * ambtition_important: What do you look for in a partner - ambition  
 * shared_interests_important: What do you look for in a partner - shared interests  
 * attractive: Rate yourself - attractiveness  
 * sincere: Rate yourself - sincerity   
 * intelligence: Rate yourself - intelligence   
 * funny: Rate yourself - being funny   
 * ambition: Rate yourself - ambition  
 * attractive_partner: Rate your partner - attractiveness  
 * sincere_partner: Rate your partner - sincerity   
 * intelligence_partner: Rate your partner - intelligence   
 * funny_partner: Rate your partner - being funny   
 * ambition_partner: Rate your partner - ambition   
 * shared_interests_partner: Rate your partner - shared interests  
 * sports: Your own interests [1-10]  
 * tvsports  
 * exercise  
 * dining  
 * museums  
 * art  
 * hiking  
 * gaming  
 * clubbing  
 * reading  
 * tv  
 * theater  
 * movies  
 * concerts  
 * music  
 * shopping  
 * yoga  
 * interests_correlate: Correlation between participant’s and partner’s ratings of interests.  
 * expected_happy_with_sd_people: How happy do you expect to be with the people you meet during the speed-dating event?  
 * expected_num_interested_in_me: Out of the 20 people you will meet, how many do you expect will be interested in dating you?  
 * expected_num_matches: How many matches do you expect to get?  
 * like: Did you like your partner?  
 * guess_prob_liked: How likely do you think it is that your partner likes you?   
 * met: Have you met your partner before?  
 * decision: Decision at night of event.
 * decision_o: Decision of partner at night of event.  
 * match: Match (yes/no)
