import bentoml
from bentoml.io import JSON
from pydantic import BaseModel

class DatingQuery(BaseModel):
    gender: str
    age: float
    age_o: float
    importance_same_religion: float
    pref_o_attractive: float
    pref_o_sincere: float
    pref_o_intelligence: float
    pref_o_funny: float
    pref_o_ambitious: float
    pref_o_shared_interests: float
    attractive_o: float
    sinsere_o: float
    intelligence_o: float
    funny_o: float
    ambitous_o: float
    shared_interests_o: float
    attractive_important: float
    sincere_important: float
    intellicence_important: float
    funny_important: float
    ambtition_important: float
    shared_interests_important: float
    attractive: float
    sincere: float
    intelligence: float
    funny: float
    ambition: float
    attractive_partner: float
    sincere_partner: float
    intelligence_partner: float
    funny_partner: float
    ambition_partner: float
    shared_interests_partner: float
    sports: float
    tvsports: float
    exercise: float
    dining: float
    museums: float
    art: float
    hiking: float
    gaming: float
    clubbing: float
    reading: float
    tv: float
    theater: float
    movies: float
    concerts: float
    music: float
    shopping: float
    yoga: float
    interests_correlate: float
    expected_happy_with_sd_people: float
    expected_num_interested_in_me: float
    expected_num_matches: float
    like: float
    guess_prob_liked: float
    met: float
    decision: float


model_ref = bentoml.xgboost.get("dating_service:latest")
dv = model_ref.custom_objects['dictVectorizer']

model_runner = model_ref.to_runner()

svc = bentoml.Service("dating_app", runners = [model_runner])

@svc.api(input=JSON(pydantic_model=DatingQuery),output=JSON())

def predict(query):
    query_data = query.dict()
    vector = dv.transform(query_data)
    prediction = model_runner.predict.run(vector)
    print(prediction)
    result = prediction[0]
    if result > 0.5:
        return {"reply":"MATCH"}
    else:
        return {"reply":"NO_MATCH"}
