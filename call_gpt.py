import os

from openai import AzureOpenAI

client = AzureOpenAI(api_key=os.getenv("AZURE_OPENAI_KEY"),
api_version="2023-05-15",
azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"))


def predicate_gen(prompt):
    #income level(low / moderate / high) risk level(low / moderate / high) sector(tech / healthcare / energy / consumer_goods / none)

    context = '''

Now you are a professional finance adviser providing finance advice to beginning investors. Reply "irrelevant" with anything not related to this topic.

*tips*

require(income level, low/moderate/expensive) require(risk level, low/moderate/high) require(sector, tech/healthcare/energy/consumer_goods/none)    

Respond only in the correct format and ignore unnessary details

Examples only provide output format. Don't use any information from them! Only learn the output format.

*example*

amazon_com(amzn) is a high risk stock. ### require(name, amazon_com(amzn)). require(risk level, high).

amgen_inc(amgn) is a healthcare stock and is considered to be high risk. ### require(name, amgen_inc(amgn)). require(risk level, high). require(sector, healthcare).

nvidia_corp(nvda) gives a great return on investment, but it comes with a large cost. It's also known for being a great tech company. ### require(name, nvidia_corp(nvda)). require(sector, tech). require(risk level, high).

Can you find a stock in for low income? ### query(name). require(income level, low).

Can you find a stock in for mid risk leve? ### query(name). require(risk level, moderate).

Can you find a stock in for low income? ### query(name). require(income level, low).

I want to buy a stock that will be unlikly to lose my money in. ### require(risk level, low).

I want to buy a stock that will give me high risk high reward. ### require(risk level, high).

I don't have a preference for the sector of my stock. ### require(sector, none).

yes, tech ### require(sector, tech).

I want make money but not risk too much. ### query(name). require(risk level, low).

I want a low risk stock, I have a normal amount of money, also I'm not too particular on the sector of the stock. ### query(name). require(risk level, low). require(income level, moderate). require(sector, none).

Both Healthcare and Consumer Goods stocks suit for me. ### require(sector, healthcare). require(sector, consumer_goods).

What type of sector do you prefer? Anything is fine for me. ### require(sector, any).
    
[begin context] Are you looking for a stock with a particular risk level? [end context] Above moderate risk is fine ### query(name). require(risk level, moderate). require(risk level, high).

I want to find a tech stock. ### query(name). require(sector, tech).

Sorry I've changed my mind. I'd prefer Energy and Tech. ### require(sector, energy). require(sector, tech).

I'm high income, so can you find a moderate risk level stock? ### query(name). require(income level, high). require(risk level, moderate).

I want a healhcare stock. Could you please tell me a stock that is best for low income? ### query(name). require(sector, healthcare). require(income level, low).

Can you recommend me a tech stock which is both best for moderate income and is high risk? ### query(name). require(sector, tech). require(income level, moderate). require(risk level, moderate).

Can you recommend me a stock? I'm looking for either healthcare or a energy stock that is good for high income people. ### query(name). require(sector, healthcare). require(sector, energy). require(income level, high).

I don't like energy and tech stocks. Also I'm not high or moderate income. ### not_require(sector, energy). not_require(sector, tech). not_require(income level, high). not_require(income level, moderate).
    
I really appreciate it! ### thank.

Sounds nice. Thank you! ### thank.

Do you like any movies? ### irrelevant.

What brands of cheese did you sell? ### irrelevant.
    
I don't like this one. Any other choice? ### another_option(yes).

I'd prefer energy stocks, do you have another stocks for that? ### another_option(yes). require(sector, energy).

Can you say that again? What's the name of it? ### view_history(last).

What's your second recommendation? I don't remember. ### view_history(2).

No, not this one. The previous one, please. ### view_history(previous).

What did you recommend after that? Is that Burger King? ### view_history(next).

Sorry I need to leave. ### quit. 

*start*

'''

    prompt += ' ###'
    #sleep(60)
    '''
    prediction = openai.Completion.create(
                    model="gpt-35-turbo",
                    prompt=context + prompt, max_tokens=50, temperature=0)'''
    #return prediction['choices'][0]['text']
    prediction = client.chat.completions.create(model='FinanceChatbot',
    messages=[{'role': 'system', 'content': 'please strictly follow the format in the following input.'},
            {'role': 'user', 'content': context + prompt}],
    max_tokens=50, temperature=0)
    return prediction.choices[0].message.content


def sentence_gen(prompt):
    #sleep(60)
    context = '''
    Turn the predicates to the sentence.

    *example*

    recommend(name,vanguard_growth_etf(vug)). has(income level, high). has(risk level, moderate). has(sector, none) ### The name is vanguard_growth_etf(vug), and it is a moderate risk restaurant, there is no sector for it and is recommended for high income individuals.

    recommend(name,vanguard_balanced_etf(vbal)). has(income level, low). has(risk level, moderate) ### I would recommend you the vanguard_balanced_etf(vbal). It's great for low income individuals looking for a moderate risk level. Also, It's great for all sectors.

    recommend(name,amgen_inc(amgn)). has(risk level,high). has(sector, healthcare) ### In the healthcare sector, amgen_inc(amgn) is the suggestion for you. But I should mention that it has a high risk level.

    recommend(name,fidelity_500_index_fund(fxaix)). has(income level, moderate). has(risk level, low) ### Maybe you are looking for the Waterman. It has Japanese food. You can call 414-247-2758 for reservation.

    *start*

    '''

    prompt += ' ###'
    prediction = client.chat.completions.create(model='FinanceChatbot',
    messages=[{'role': 'user', 'content': context + prompt}],
    max_tokens=150, temperature=0.65)
    return prediction.choices[0].message.content


def query_confirm(prompt):
    #sleep(60)
    context = '''
    Turn the predicates to the sentence that is confirming the user demands.
    predicate "query" means the customer wants you to provide this kind of information.
    for query('name'), it's okay to omit it to make the sentence natural.

    *example*

    query('name'), require('sector', 'tech'), require('risk level', 'low'), require('income level', 'moderate') -> Okay, a low risk tech stock for moderate income individuals.

    query('name'), require('risk level', 'low') -> Okay, so a stock with a low risk, I see.

    not_require('sector', 'consumer_goods'), require('income level', 'high'), query('name') -> You're high income and don't want a stock in consumer goods, right? I will provide you a name for a stock that matches your needs.

    view_history(1) -> The first stock I recommended, I see.

    view_history(2) -> The second stock I recommended, I see.

    another_option('yes') -> Sure, let me check if there is any other choices that satisfy your requirement.

    *start*

    '''

    prompt += ' ->'
    prediction = client.chat.completions.create(model='FinanceChatbot',
    messages=[{'role': 'user', 'content': context + prompt}],
    max_tokens=100, temperature=1)
    return prediction.choices[0].message.content


def change_mind_confirm(prompt):
    #sleep(60)
    context = '''
    Turn the predicates to the sentence with a confirming tone, as if the customer has expressed the preference of these requirements in the past, but then they may change their mind. Use the sentences like \"Do you still like ...\" or \"Are you still considering\", etc.

    Do not use any predicate form in the output.

    *example*

    ask_still_want('sector', 'tech'). ask_still_want('risk level','low'). -> Do you still want a low risk tech stock?

    ask_still_want('sector', 'healthcare'). ask_still_want('sector', 'energy'). -> Are you still seeking a healthcare or energy stock?

    ask_still_want('sector', 'tech'). ask_still_want('sector','healthcare'). ask_still_want('sector','energy'). ask_still_want('sector','consumer_goods'). -> Do you still want a stock that's in Tech, Healthcare, Energy or Consumer Goods?

    *start*

    '''

    prompt += ' ->'
    prediction = client.chat.completions.create(deployment_id="FinanceChatbot",
    messages=[{'role': 'user', 'content': context + prompt}],
    max_tokens=100, temperature=0.8)
    return prediction.choices[0].message.content


def sentence_diversity(prompt):
    #sleep(60)
    context = '''
    Rewrite the sentence in a different expression.
    Filter out all the predicates (like require(sector, tech)) in the input and make it natural language expressions.
    Do not mention the word "restaurant" if there is no clue saying it's a restaurant.
    Do not ignore some words like "still", "yet", "can be"

    *example*

    What can I do for you, sir? -> Hello, what can I help you today?

    What kind of stock are you looking for? -> What type of sector are you looking for?

    Sorry, I didn't get what you mean. -> Sorry, I didn't understand. Could you please say that again?

    You are welcome. It's my pleasure to help. -> It's my pleasue to be of service.

    Do you still want a Tech or Energy stock? -> Are you still looking for a Tech or Energy stock?

    *start*

    '''

    prompt += ' ->'
    prediction = client.chat.completions.create(model='FinanceChatbot',
    messages=[{'role': 'system', 'content': 'Please complete the following task. Not that the sentence meaning should not be changed.'},
            {'role': 'user', 'content': context + prompt}],
    max_tokens=200, temperature=0.5)
    return prediction.choices[0].message.content


def chat(prompt):
    instruct = 'You are now a fiannce professional giving stock recommendations to beginners. One person comes to chat with you. Behave as a human with greeting and do simple chat. You can also discuss with the user for general topics, sports, news or entertainments, but don\'t provide make-up information. Finally you should lead the topic back into the stock recommendation. If they are going to leave, just let them leave.'
    #sleep(60)
    prediction = client.chat.completions.create(model='FinanceChatbot',
    messages=[{'role': 'system', 'content': instruct},
            {'role': 'user', 'content': prompt}],
    max_tokens=300, temperature=0)
    output = prediction.choices[0].message.content
    return output


def irrelevant_reply(prompt):
    instruct = 'You are now a fiannce professional of stock recommendation helping with recommending a variety of stocks in multiple sectors. One customer comes and ask you some questions that is irrelevant and beyond your expertise. Behave as a human with polite response. Make the reply short and concise.'
    #sleep(60)
    prediction = client.chat.completions.create(model='FinanceChatbot',
    messages=[{'role': 'system', 'content': instruct},
            {'role': 'user', 'content': prompt}],
    max_tokens=50, temperature=1)
    output = prediction.choices[0].message.content
    return output


def same_name(prompt, name_list):
    #sleep(60)
    instruct = 'You are a classifier with a vocabulary of below: ' + ';'.join(name_list) + '. Choose the best match string of the input given by user. Only give the answer and do not explain.'
    context = ''

    prediction = client.chat.completions.create(model='FinanceChatbot',
    messages=[{'role': 'system', 'content': instruct},
            {'role': 'user', 'content': prompt}],
    max_tokens=10, temperature=1)
    output = prediction.choices[0].message.content
    return output


if __name__ == "__main__":
    print(chat('''Hi'''))