# Environment URLs
DEV_ENV_URL = 'http://dev.api.bkstg.com/api'
MASTER_ENV_URL = 'https://bkstg_api_master.aws.bkstg.com/api'


# Auth URLs
AUTH_LOGIN = '/auth/login'
AUTH_SIGN_UP = '/auth/register'
AUTH_LOGOUT = '/auth/logout'
AUTH_CHECK_EMAIL = '/auth/check/email'
AUTH_CHECK_NAME = '/auth/check/username'
AUTH_CHANGE_PASSWORD = '/auth/password/change'
AUTH_FORGOT_PASSWORD = '/auth/password/forgot'
AUTH_FB_LOGIN = '/auth/fb/login'

# Accounts URLs
ACCOUNT_USER = '/accounts/me'
ACCOUNT_SUBSCRIPTIONS = '/accounts/me/subscriptions'
ACCOUNT_USER_SUBSCRIPTIONS = '/accounts/%s/subscriptions'
ACCOUNT_SUBSCRIBE_HUB = '/accounts/me/subscriptions/%s'
ACCOUNT_FOLLOWERS = '/accounts/%s/followers'
ACCOUNT_FOLLOW_USER = '/accounts/me/follows/%s'
ACCOUNT_FOLLOWING = '/accounts/%s/following'
ACCOUNT_USER_ROLE_FOR_HUB = '/accounts/%s/roles/%s'
ACCOUNT_LINK_ACCOUNTS = '/accounts/%s/links/%s/hubs/%s'
ACCOUNT_PROFILE = '/accounts/%s'
ACCOUNT_LINKED_ACCOUNTS_LIST = '/accounts/me/linked-accounts/%s'
ACCOUNT_LOYALTY_LEVEL = '/accounts/%s/loyalty/%s'
ACCOUNT_USER_PERMISSION_GROUPS = '/accounts/%s/permissions/%s'
ACCOUNT_USER_PERMISSION_GROUP_RELATION = '/accounts/%s/permissions/%s/groups/%s'
ACCOUNT_SNS_ENDPOINT = '/accounts/me/endpoints/%s'
ACCOUNT_PUSH = '/accounts/%s/push'
ACCOUNT_RESEND_VERIFICATION_EMAIL = '/accounts/me/resend-verification-email'
ACCOUNT_CONNECT_FACEBOOK = '/accounts/me/connect/fb'
ACCOUNT_PROFILE_BY_ADMIN = '/accounts/%s/profile-admin/%s'
ACCOUNT_BAN = '/accounts/%s/ban'

# Community URLs
COMMUNITY_USER_POSTS = '/community/posts?author_id=%s'
COMMUNITY_HUB_POSTS = '/community/%s/posts'
COMMUNITY_HUB_POST = '/community/%s/posts/%s'
COMMUNITY_HUB_INAPPROPRIATE_POST = '/community/%s/posts/%s/inappropriate'
COMMUNITY_HUB_LIKE_POST = '/community/%s/posts/%s/likes'
COMMUNITY_HUB_LIKERS = '/community/%s/posts/%s/likes'
COMMUNITY_HUB_POST_COMMENTS = '/community/%s/posts/%s/comments'
COMMUNITY_HUB_POST_COMMENT = '/community/%s/posts/%s/comments/%s'
COMMUNITY_HUB_INAPPROPRIATE_POST_COMMENT = '/community/%s/posts/%s/comments/%s/inappropriate'
COMMUNITY_HUB_PIN_POST = '/community/%s/posts/%s/pin'

# Moderation URLs
INAPPROPRIATE_WORDS_LIST = '/moderation/%s/words'
INAPPROPRIATE_WORD = '/moderation/%s/words/%s'
REPORTED_CONTENT = '/moderation/%s/list'
INAPPROPRIATE_ITEM = '/moderation/%s/%s/%s'

# Hubs URLs
HUBS_LIST = '/hubs/hubs'
ADMIN_HUBS_LIST = '/hubs/hubs-admin'
HUB = '/hubs/hubs/%s'
EDIT_HUB = '/hubs/hubs/%s'
GHOST_HUB = '/hubs/ghost'
HUB_SETTINGS = '/hubs/hubs/%s/settings'
HUB_SIGNATURE = '/hubs/%s/signature'
HUB_CELEBRITY_SIGNATURE = '/hubs/%s/signature/%s'
HUB_SIGN_HUB = '/hubs/%s/user-hub-signature/%s'
HUB_TEAM = '/hubs/%s/team'
HUB_TEAM_ALIASES = '/hubs/%s/aliases'
HUB_TEAM_ALIAS = '/hubs/%s/aliases/%s'
HUB_TEAM_LINK_ALIAS = '/hubs/%s/aliases/%s/users/%s'
HUB_SEARCH = '/hubs/%s/search-users'
HUB_ADMIN = '/hubs/hubs-admin/%s'

# Feed URLs
FEED_POSTS_LIST = '/feed/%s/posts'
FEED_POSTS_LIST_FOR_ADMIN = '/feed/%s/posts-admin'
FEED_POST_FOR_ADMIN = '/feed/%s/posts-admin/%s'
FEED_SWITCH_POST = '/feed/%s/posts/%s/switch/%s'
FEED_POST = '/feed/%s/posts/%s'
FEED_POST_LIKES = '/feed/%s/posts/%s/likes'
FEED_POST_COMMENTS_LIST = '/feed/%s/posts/%s/comments'
FEED_POST_COMMENT = '/feed/%s/posts/%s/comments/%s'
FEED_REPORT_INAPPROPRIATE_COMMENT = '/feed/%s/posts/%s/comments/%s/inappropriate'
FEED_PIN_POST = '/feed/%s/posts/%s/pin'
FEED_AUTHORS = '/feed/%s/authors'
FEED_PUSHES = '/feed/%s/push-messages/%s'

# Media URLs
MEDIA_AFTER_UPLOAD = '/media/afterupload'
MEDIA_EXT_RESOURCE = '/media/external'
MEDIA_SANDBOX = '/media/sandbox'
MEDIA_HUB_EXT_RESOURCE = '/media/%s/external'
MEDIA_ITEMS_LIST = '/media/items'
MEDIA_ITEM_THUMBNAIL = '/media/items/%s/thumbnail'
MEDIA_ITEM_PREVIEW = '/media/items/%s/preview'
MEDIA_IMAGE_ALBUMS = '/media/hub/%s/image/albums?private=true'
MEDIA_AUDIO_ALBUMS = '/media/hub/%s/audio/albums?private=true'
MEDIA_VIDEO_ALBUMS = '/media/hub/%s/video/albums?private=true'
MEDIA_IMAGE_ALBUM = '/media/hub/%s/image/albums/%s'
MEDIA_AUDIO_ALBUM = '/media/hub/%s/audio/albums/%s'
MEDIA_VIDEO_ALBUM = '/media/hub/%s/video/albums/%s'
MEDIA_ALBUM_ATTACH_IMAGE_ITEMS = '/media/hub/%s/image/albums/%s/attach/items'
MEDIA_ALBUM_ATTACH_AUDIO_ITEMS = '/media/hub/%s/audio/albums/%s/attach/items'
MEDIA_ALBUM_ATTACH_VIDEO_ITEMS = '/media/hub/%s/video/albums/%s/attach/items'
MEDIA_ALBUM_IMAGE_ITEMS = '/media/hub/%s/image/albums/%s/items'
MEDIA_ALBUM_AUDIO_ITEMS = '/media/hub/%s/audio/albums/%s/items'
MEDIA_ALBUM_VIDEO_ITEMS = '/media/hub/%s/video/albums/%s/items'
MEDIA_HUB_IMAGE_ITEMS = '/media/hub/%s/image/items'
MEDIA_HUB_AUDIO_ITEMS = '/media/hub/%s/audio/items'
MEDIA_HUB_VIDEO_ITEMS = '/media/hub/%s/video/items'
MEDIA_HUB_ATTACH_IMAGE_ITEMS = '/media/hub/%s/image/attach/items'
MEDIA_HUB_ATTACH_AUDIO_ITEMS = '/media/hub/%s/audio/attach/items'
MEDIA_HUB_ATTACH_VIDEO_ITEMS = '/media/hub/%s/video/attach/items'
MEDIA_HUB_IMAGE_ALBUM = '/media/hub/%s/image/albums/%s'
MEDIA_HUB_AUDIO_ALBUM = '/media/hub/%s/audio/albums/%s'
MEDIA_HUB_VIDEO_ALBUM = '/media/hub/%s/video/albums/%s'

# Permissions URLs
PERMISSION_GROUPS_LIST = '/permissions/groups'
PERMISSION_GROUP = '/permissions/groups/%s'
PERMISSION_GROUP_PERMISSIONS_LIST = '/permissions/groups/%s/permissions'
PERMISSION_GROUP_SET_PERMISSION = '/permissions/groups/%s/permissions/%s'

# Settings
SETTINGS_APPLICATION = '/settings'
SETTINGS_HUB = '/settings/%s'

# Static Pages URLs
STATIC_TC_PAGE = '/static-pages/terms-and-conditions'

# Store URLs
STORE_PRODUCTS = '/store/hub/%s/products'

# Tickets URLs
TICKETS_HUB_TOUR = '/tickets/hub/%s'
TICKETS_TOUR = '/tickets/tour/%s'
TICKETS_TOUR_CONCERTS = '/tickets/tour/%s/concerts'

# URL Shortener
URL_SHORTENER = '/shortener/code'
URL_SHORTENER_PARAMS = '/shortener/code/%s'
