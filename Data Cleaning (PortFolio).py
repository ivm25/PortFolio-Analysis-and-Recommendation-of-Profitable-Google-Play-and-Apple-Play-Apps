#!/usr/bin/env python
# coding: utf-8

# ### Table of Contents
# ***
# 1 [DEFINE](#definition)
# 
# 1.1 [BUSINESS PROBLEM](#problem)
# 

# ### 1: DEFINE
# <a id="definition"></a>

# We only build apps that are free to download and install, and our main source of revenue consists of in-app ads. This means our revenue for any given app is mostly influenced by the number of users who use our app — the more users that see and engage with the ads, the better

# ### 1.1 BUSINESS PROBLEM
# <a id="problem"></a>

# To analyze data to help our developers understand what type of apps are likely to attract more users.

# In[5]:


from csv import reader
dataset=open('AppleStore.csv',encoding='utf8')
Applestore_dataset=reader(dataset)
Applestore_dataset_list=list(Applestore_dataset)


# In[6]:


dataset_1=open('googleplayStore.csv',encoding='utf8')
googleplaystore_dataset=reader(dataset_1)
googleplay_dataset_list=list(googleplaystore_dataset)


# In[7]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[9]:


explore_data(Applestore_dataset_list,0,6,rows_and_columns=True)


# In[10]:


explore_data(googleplay_dataset_list,0,6,rows_and_columns=True)


# In[13]:


print(googleplay_dataset_list[10473])


# In[15]:


del(googleplay_dataset_list[10473])


# In[16]:


print(googleplay_dataset_list[10473])


# In[60]:


unique_app=[]
duplicate_app=[]
for app in googleplay_dataset_list:
    name=app[0]
    if name in unique_app:
        duplicate_app.append(name)
    else:
        unique_app.append(name)
        
    


# In[61]:


print("The number of Unique apps in googleplaystore are:", len(unique_app))
print("\n")
print("The number of Duplicate apps in googleplaystore are:", len(duplicate_app))


# ### Criteria for removing duplicate apps
# 
# The number of reviews for same app differ as the reviews posted most recently are more correct. 

# In[67]:


reviews_max={}

for row in googleplay_dataset_list[1:]:
    name=row[0]
    n_reviews=float(row[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    if name not in reviews_max:
        reviews_max[name] = n_reviews
        
        




# In[68]:


print(len(reviews_max))


# ## Creating list of apps without any duplicates

# In[69]:


android_clean=[]
already_added=[]

for row in googleplay_dataset_list[1:]:
    name=row[0]
    n_reviews=float(row[3])
    if n_reviews==reviews_max[name] and name not in already_added:
        android_clean.append(row)
        already_added.append(name)


# In[70]:


print(len(android_clean))
print(len(already_added))


# In[116]:


print(android_clean)


# ## Removing Non English Apps from the dataset

# **Removing Non English Apps, with a condition that if more than 3 characters have an ASCII score above 127, they will be removed.**
# 

# In[111]:


def nonenglish(s):
    num=0
    for character in s:
        
        if ord(character)>127:
            print(ord(character))
            num += 1
    if num > 3:
        return False
            
    else:
        return True


# In[114]:


nonenglish('Docs To Go™ Free Office Suite')


# In[112]:


nonenglish('爱奇艺PPS -《欢乐颂2》电视剧热播')


# **Using the function above to eliminate Non English Apps from both the datasets and appending to a new list.**

# In[119]:


English_Apps=[]

for row in android_clean:
    name=row[0]
    if nonenglish(name)==True:
        English_Apps.append(row)
    


# In[120]:


English_Apps


# In[121]:


len(English_Apps)


# In[122]:


English_Apps_Apple=[]

for row in Applestore_dataset_list[1:]:
    name=row[0]
    if nonenglish(name)==True:
        English_Apps_Apple.append(row)
    


# In[123]:


English_Apps_Apple


# ## Identifying Free apps for both the datasets

# In[127]:


Free_Apps=[]

for row in English_Apps:
    price=row[6]
    if price=='Free':
        Free_Apps.append(row)
    


# In[128]:


Free_Apps


# In[137]:


Free_Apps_Apple=[]

for row in English_Apps_Apple:
    price=row[4]
    if price=='0.0':
        Free_Apps_Apple.append(row)
    


# In[138]:


Free_Apps_Apple


# In[140]:


print('Length of Free Google Apps is:',len(Free_Apps))
print('\n')
print('Length of Free Apple Apps is:',len(Free_Apps_Apple))


# ### Out of all tg free apps, we need to identify apps that would work for both googlestore and applestore. In a way, identify genres that would generate revenue, like gamification apps.
# 
# ** We will create frequency tables from the free apps lists to identify most common genres**
# 

# The display table function builds on top of the frequency table and prints out a sorted tuple to identify the maximum dict value.
# 
# **Takes in two parameters: dataset and index. dataset is expected to be a list of lists, and index is expected to be an integer.
# Generates a frequency table using the freq_table() function (which you're going to write as an exercise).
# Transforms the frequency table into a list of tuples, then sorts the list in a descending order.
# Prints the entries of the frequency table in descending order**

# In[156]:


def freq_table(dataset,index):

    freq={}
    for row in dataset:
        var=row[index]
        if var in freq:
            freq[var] += 1
        else:
            freq[var] = 1
    return freq




def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[157]:


# Printing the Genre column from the google dataset as a tuple:

freq_table(Free_Apps,9)
display_table(Free_Apps,9)


# In[159]:


# Printing the Category column from the google dataset as a tuple:

freq(Free_Apps,1)
display_table(Free_Apps,1)


# In[158]:


# Printing the Prime Genre column from the Apple dataset as a tuple:

freq(Free_Apps_Apple,11)
display_table(Free_Apps_Apple,11)


# Analyze the frequency table you generated for the prime_genre column of the App Store data set.
# ---
# **What is the most common genre? What is the runner-up?**
# 
#   The most common genre is Games, followed by Entertainment, Photo and Video.
#   
# **What other patterns do you see?**
# 
#   Gaminng and Entertainment apps tend to dominate the Apple store profile. Fewer genres of Education, Business.
#   
# **What is the general impression — are most of the apps designed for practical purposes (education, shopping, utilities, productivity, lifestyle) or more for entertainment (games, photo and video, social networking, sports, music)?**
# 
#   Most of them are for Entertainment purposes.
#   
# **Can you recommend an app profile for the App Store market based on this frequency table alone? If there's a large number of apps for a particular genre, does that also imply that apps of that genre generally have a large number of users?**
# 
#   An app profile wuld be gaming oriented, yet entertaining. Not necessarily it means that a large number of Gaming Genres will have a higher number of Users, that is something that needs further analysis. 

# Analyze the frequency table you generated for the Category and Genres column of the Google Play data set.
# ---
# 
# **What are the most common genres?**
# 
# Tools, Entertainment. Within the the category, it appears that Family and Games are the most common ones.
# 
# **What other patterns do you see?**
# 
# There is a mix of entertainment based apps and ones with a practical usage. 
# 
# **Compare the patterns you see for the Google Play market with those you saw for the App Store market.**
# 
# Differs in the sense that there are no clear cut winners with respect to top genres, it is a mixed bag of entertainment and practical usage apps.
# 
# **Can you recommend an app profile based on what you found so far? Do the frequency tables you generated reveal the most frequent app genres or what genres have the most users?**
# Not right now, we need to analyse the most uers for that given genre/Category.

# In[161]:


freq_table(Free_Apps_Apple,11)


# In[180]:


genre_ratings_apple=freq_table(Free_Apps_Apple,11)

for genre in genre_ratings_apple:
    total=0
    len_genre=0
    for row in Free_Apps_Apple:
        genre_app=row[11]
        if genre_app == genre:
            rating=float(row[5])
            total += rating
            len_genre += 1
    avg_rating = total/len_genre      
    print(genre,avg_rating)


# **App Recommendation for Apple Store: Social and Networking with a high Avg_rating. **

# ## Generating frequency table for the category column of googleplay store using the function created earlier.
# 
# 

# In[182]:


genre_ratings_google=freq(Free_Apps,1)
for category in genre_ratings_google:
    total=0
    len_category=0
    for row in Free_Apps:
        category_app=row[1]
        if category_app == category:
            n_installs = row[5]
            n_installs=(n_installs.replace('+',''))
            n_installs=(n_installs.replace(',',''))
            total += float(n_installs)
            len_category += 1
    avg_rating_google = total/len_category
    print(category, avg_rating_google)

