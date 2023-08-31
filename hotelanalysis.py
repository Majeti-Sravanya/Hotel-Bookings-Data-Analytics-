#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Data Exploration


# In[1]:


import pandas as pd


# In[2]:


df_bookings = pd.read_csv("fact_bookings.csv")
df_bookings.head(4)


# In[3]:


df_bookings.shape


# In[4]:


df_bookings.room_category.unique()


# In[5]:


df_bookings.booking_platform.unique()


# In[6]:


df_bookings.booking_platform.value_counts().plot(kind="barh")


# In[7]:


df_bookings.describe()


# In[8]:


df_bookings.revenue_generated.min(),df_bookings.revenue_generated.max()


# In[9]:


df_date = pd.read_csv("dim_date.csv")
df_hotels = pd.read_csv("dim_hotels.csv")
df_rooms = pd.read_csv("dim_rooms.csv")
df_agg_bookings = pd.read_csv("fact_aggregated_bookings.csv")


# In[10]:


df_hotels.shape


# In[11]:


df_hotels.head(4)


# In[12]:


df_hotels.category.value_counts()


# In[13]:


df_hotels.city.value_counts().sort_values().plot(kind="bar")


# In[14]:


df_agg_bookings.head(5)


# In[15]:


df_agg_bookings.property_id.unique()


# In[16]:


df_agg_bookings.property_id.value_counts()


# In[17]:


df_agg_bookings.groupby('property_id')['successful_bookings'].sum()


# In[18]:


df_agg_bookings[df_agg_bookings.successful_bookings>df_agg_bookings.capacity]


# In[19]:


df_agg_bookings.capacity.max()


# In[ ]:


# Data Cleaning


# In[20]:


df_bookings.describe()


# In[21]:


df_bookings[df_bookings.no_guests<=0]


# In[22]:


df_bookings = df_bookings[df_bookings.no_guests>0]
df_bookings.shape


# In[23]:


df_bookings.revenue_generated.min(),df_bookings.revenue_generated.max()


# In[24]:


avg, std = df_bookings.revenue_generated.mean(), df_bookings.revenue_generated.std()


# In[25]:


avg, std


# In[26]:


higher_limit = avg + 3*std
higher_limit


# In[27]:


lower_limit = avg - 3*std
lower_limit


# In[28]:


df_bookings[df_bookings.revenue_generated>higher_limit]


# In[29]:


df_bookings[df_bookings.revenue_generated<higher_limit]


# In[30]:


df_bookings = df_bookings[df_bookings.revenue_generated<higher_limit]


# In[31]:


df_bookings.shape


# In[32]:


df_bookings.revenue_realized.describe()


# In[33]:


higher_limit = df_bookings.revenue_realized.mean() + 3*df_bookings.revenue_realized.std()
higher_limit


# In[34]:


df_bookings[df_bookings.revenue_realized>higher_limit]


# In[35]:


df_rooms


# In[37]:


df_bookings[df_bookings.room_category=="RT4"].revenue_realized.describe()


# In[38]:


23439 + 3*9048


# In[39]:


df_bookings.isnull().sum()


# In[40]:


df_agg_bookings[df_agg_bookings.capacity.isna()]


# In[41]:


df_agg_bookings.capacity.median()


# In[42]:


df_agg_bookings.capacity.fillna(df_agg_bookings.capacity.median(), inplace=True)


# In[43]:


df_agg_bookings.loc[[8,15]]


# In[44]:


df_agg_bookings[df_agg_bookings.successful_bookings>df_agg_bookings.capacity]


# In[45]:


df_agg_bookings.shape


# In[47]:


# Data Transformation


# In[48]:


df_agg_bookings.head()


# In[70]:


df_agg_bookings["occ_pct"] = df_agg_bookings["successful_bookings"]/df_agg_bookings["capacity"]


# In[71]:


df_agg_bookings.head()


# In[72]:


df_agg_bookings["occ_pct"] = df_agg_bookings["occ_pct"].apply(lambda x: round(x*100, 2))


# In[73]:


df_agg_bookings.head()


# In[74]:


# Insights Generation


# In[ ]:


# What is an average occupancy rate in each of the room categories ?


# In[76]:


df_agg_bookings.groupby("room_category")["occ_pct"].mean().round(2)


# In[77]:


df_rooms


# In[ ]:


df_agg_bookings


# In[83]:


df = pd.merge(df_agg_bookings, df_rooms, left_on="room_category", right_on="room_id")
df.head(4)


# In[84]:


df.tail(4)


# In[85]:


df.groupby("room_class")["occ_pct"].mean().round(2)


# In[86]:


df.drop("room_id",axis=1, inplace=True)
df.head(4)


# In[87]:


# 2 print average occupancy rate per city ?


# In[89]:


df_hotels.head(5)


# In[91]:


df = pd.merge(df,df_hotels, on="property_id")
df.head(3)


# In[92]:


df.groupby("city")["occ_pct"].mean()


# In[95]:


df.groupby("city")["occ_pct"].mean().plot(kind="bar")


# In[96]:


# 3 when was the occupancy better weekdays or weekends ?


# In[97]:


df.head(3)


# In[99]:


df_date


# In[100]:


df = pd.merge(df, df_date,left_on="check_in_date", right_on="date")
df.head(3)


# In[101]:


df.groupby("day_type")["occ_pct"].mean().round(2)


# In[102]:


# 3 in the month of june, what is the occupancy rate for differnt cities ?


# In[103]:


df["mmm yy"].unique()


# In[106]:


df_june_22 = df[df["mmm yy"]=="Jun 22"]
df_june_22.head(3)


# In[109]:


df_june_22.groupby("city")["occ_pct"].mean().round(2).sort_values(ascending=False)


# In[111]:


df_august = pd.read_csv("new_data_august.csv")
df_august.head(3)


# In[113]:


df_august.columns


# In[114]:


df.columns


# In[115]:


df_august.shape


# In[116]:


df.shape


# In[117]:


latest_df = pd.concat([df, df_august], ignore_index=True, axis=0 )
latest_df.tail(10)


# In[118]:


latest_df.shape


# In[119]:


# Print revenue realized per city


# In[120]:


df_bookings.head(4)


# In[121]:


df_hotels.head(4)


# In[122]:


df_bookings_all = pd.merge(df_bookings,df_hotels, on="property_id")
df_bookings_all.head(4)


# In[123]:


df_bookings_all.groupby("city")["revenue_realized"].sum()


# In[124]:


# Print month by month revenue


# In[125]:


df_bookings_all.head(5)


# In[126]:


df_date["mmm yy"].unique()


# In[127]:


df_date.head(5)


# In[128]:


pd.merge(df_bookings_all, df_date, left_on="check_in_date", right_on="date" )


# In[130]:


df_bookings_all.info()


# In[131]:


df_date.info()


# In[133]:


df_date["date"] = pd.to_datetime(df_date["date"])
df_date.head(3)


# In[144]:


df_date.info()


# In[148]:


df_bookings_all.head(3)


# In[149]:


df_bookings_all.info()


# In[152]:


#Print revenue realized per hotel type


# In[154]:


df_bookings_all.property_name.unique()


# In[156]:


df_bookings_all.groupby("property_name")["revenue_realized"].sum().round(2).sort_values()


# In[157]:


#Print average rating per city


# In[158]:


df_bookings_all.groupby("city")["ratings_given"].mean().round(2)


# In[159]:


#Print a pie chart of revenue realized per booking platform


# In[160]:


df_bookings_all.groupby("booking_platform")["revenue_realized"].sum().plot(kind="pie")


# In[ ]:




