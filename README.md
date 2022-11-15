<h1>REST API methods</h1>

get_profile/username/ - returns user data by given nickname;

get_sub_videos/ - returns videos of users that the current user is subscribed to (if the request method is GET), adds a new video (if the request method is POST);

get_sub_videos/ - returns latest videos (if the request method is GET), adds a new video (if the request method is POST);

get_video/video_id - returns video data by given comment id (if the request method is GET), deletes video (if the request method is DELETE);

get_comments/video_id - returns all comments to the given video (if the request method is GET), creates a new comment (if the request method is POST);

get_comment/comment_id - returns comment data by given comment id (if the request method is GET), deletes comment (if the request method is DELETE);

get_likes/video_id - returns all likes to the given video (if the request method is GET), adds like (if the request method is POST);

get_like/like_id - returns like data by given like id (if the request method is GET), deletes like (if the request method is DELETE);

get_subscribtions/username - returns all subscribtions to the given username (if the request method is GET), creates subscribtions (if the request method is POST);

get_subscribtion/subscribtion_id - returns subscribtion data by given subscribtion id (if the request method is GET), deletes subscribtion (if the request method is DELETE);

get_bans/username - returns all bans by the given username (if the request method is GET), adds ban (if the request method is POST);

get_ban/ban_id - returns ban data by given ban id (if the request method is GET), deletes ban (if the request method is DELETE);



