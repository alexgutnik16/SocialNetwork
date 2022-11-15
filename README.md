<h1>REST API methods</h1>

<h3>get_profile/username/</h3> - returns user data by given nickname;

<h3>get_sub_videos/</h3> - returns videos of users that the current user is subscribed to (if the request method is GET), adds a new video (if the request method is POST);

<h3>get_sub_videos/</h3> - returns latest videos (if the request method is GET), adds a new video (if the request method is POST);

<h3>get_video/video_id</h3> - returns video data by given comment id (if the request method is GET), deletes video (if the request method is DELETE);

<h3>get_comments/video_id</h3> - returns all comments to the given video (if the request method is GET), creates a new comment (if the request method is POST);

<h3>get_comment/comment_id</h3> - returns comment data by given comment id (if the request method is GET), deletes comment (if the request method is DELETE);

<h3>get_likes/video_id</h3> - returns all likes to the given video (if the request method is GET), adds like (if the request method is POST);

<h3>get_like/like_id</h3> - returns like data by given like id (if the request method is GET), deletes like (if the request method is DELETE);

<h3>get_subscribtions/username</h3> - returns all subscribtions to the given username (if the request method is GET), creates subscribtions (if the request method is POST);

<h3>get_subscribtion/subscribtion_id</h3> - returns subscribtion data by given subscribtion id (if the request method is GET), deletes subscribtion (if the request method is DELETE);

<h3>get_bans/username</h3> - returns all bans by the given username (if the request method is GET), adds ban (if the request method is POST);

<h3>get_ban/ban_id</h3> - returns ban data by given ban id (if the request method is GET), deletes ban (if the request method is DELETE);



