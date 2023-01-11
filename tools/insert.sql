INSERT INTO temp (

    admin,

    type_lambda_delta, type_epsilon_subcycle_delta, follower_delta,
    following_delta, type_alpha_delta,

    playlist_delta, ystream_delta, blog_delta,

    destroyer_delta, inactive_delta,

    unfriend_delta, friend_delta, type_gamma_delta, mention_delta, 
    tweet_delta, reply_type1_delta, reply_type2_delta,

    type_epsilon_supercycle_index, type_epsilon_subcycle_index,
    tweetAI_subcycle_index, unfriend_subcycle_index, friend_subcycle_index,
    playlist_subcycle_index, ystream_subcycle_index,

    tweetHardcoded_index, tweetMeme_index, type_lambda_index, playlist_index,
    ystream_index, blog_index, type_alpha_index, inactive_index, destroyer_index,
    tfilter_index,

    tweetAI_injection_state, follower_pagination, following_pagination,
    
    follower_count, following_count, unfriendQ_count, unfriend_count, 
    friendQ_count, friend_count,

    type_alpha_count,

    like_subcycle_count, retweet_reply_count, tweet_count, reply_count, 
    like_count,

    follower_complete, following_complete,

    like_probability, reply_probability, retweet_probability, 
    reply_probability_type2, 
    
    tweetAI_prompt_index) 

SELECT admin, tweetScraper_delta, tweetScraper_type2_subcycle_delta, 
follower_delta, following_delta, scraper_delta, playlist_delta, ystream_delta, 
blog_delta, destroyer_delta, inactive_delta, unfriend_delta, friend_delta, 
gamma_scraper_delta, mention_delta, tweet_delta, reply_type1_delta, 
reply_type2_delta, tweetScraper_type2_supercycle_index, 
tweetScraper_type2_subcycle_index, tweetAI_subcycle_index, 
unfriend_subcycle_index, friend_subcycle_index, playlist_subcycle_index, 
ystream_subcycle_index, tweetHardcoded_index, tweetMeme_index, 
tweetScraper_index, playlist_index, ystream_index, blog_index, scraper_index, 
inactive_index, destroyer_index, tfilter_index, tweetAI_injection_state, 
follower_pagination, following_pagination, follower_count, following_count, 
unfriendQ_count, unfriend_count, friendQ_count, friend_count, scraper_count,
like_subcycle_count, retweet_reply_count, tweet_count, reply_count, like_count,
follower_complete, following_complete, like_probability, reply_probability, 
retweet_probability, reply_probability_type2, tweetAI_prompt_index FROM state; 
