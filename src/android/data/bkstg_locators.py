# -------------------------------------Auth Page--------------------------------------
# By ID
EMAIL_BUTTON = 'com.bkstg:id/btn_choice_email'
FACEBOOK_BUTTON = 'com.bkstg:id/btn_choice_fb'
EMAIL_FIELD = 'com.bkstg:id/obn_field_edittext'
NEXT_BUTTON = 'com.bkstg:id/onb_next_btn'
COOL_BUTTON = 'com.bkstg:id/splash_cool_btn_text'
SIGN_UP_BUTTON = 'com.bkstg:id/onb_next_btn'

# By xpath
PASSWORD_FIELD = '//android.widget.ScrollView/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.EditText'
NICKNAME_FIELD = '//android.widget.ScrollView/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[3]/android.widget.EditText'
FIRST_LAST_NAME_FIELD = '//android.widget.EditText[@text="FIRST & LASTNAME"]'

# -------------------------------------Main Page--------------------------------------\==\
# By ID
SEARCH_FIELD = 'com.bkstg:id/search_view'
CANCEL_SEARCH = 'com.bkstg:id/search_cancel_button'
EXPLORE_CARD = 'com.bkstg:id/abstract_card_cover'
NOTIFY_BUTTON = 'android:id/button1'
DELETE_HUB_BUTTON = 'com.bkstg:id/remove_card_button'
# ADD_HUB_BUTTON = 'com.bkstg:id/explore_card_add_button'

# By xpath
ADD_HUB_BUTTON = '//android.widget.TextView[@text="%s"]/following::android.widget.ImageView'
CARD_TITLE = '//android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@text="%s"]'


# -------------------------------------Feed Page--------------------------------------
# By ID
COMMENT_BUTTON = 'com.bkstg:id/btn_post_action_comment'
COMMENT_FIELD = 'com.bkstg:id/comments_edit'
SEND_COMMENT_BUTTON = 'com.bkstg:id/comments_send_btn'
CLOSE_COMMENTS_BUTTON = 'com.bkstg:id/comments_close_btn'
LIKE_BUTTON = 'com.bkstg:id/btn_like_post'
COMMENT_COUNT = 'com.bkstg:id/txt_comments_count'
LIKE_COUNT = 'com.bkstg:id/txt_likers_count'
CREATION_TOOLS_BUTTON = 'com.bkstg:id/fab'
UPLOAD_POST_MESSAGE = 'com.bkstg:id/textViewMessage'
BKSTG_SUB_MENU = 'com.bkstg:id/bkstgButton'
SHARE_BUTTON = 'com.bkstg:id/btn_post_action_share'


# By xpath
COMMENT_TEXT = '//android.widget.TextView[@text="%s"]'
# BKSTG_SUB_MENU_ITEM = '//android.widget.TextView[@text="%s"]'
SHARE_WAY = '//android.widget.ListView/android.widget.TextView[@text="%s"]'
BKSTG_SUB_MENU_ITEM = '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[%s]/android.widget.ImageView'
VERIFY_SUB_MENU_ITEM = '//android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.RelativeLayout[1]/android.widget.RelativeLayout/android.widget.TextView'

# -------------------------------------Creations tools---------------------------------
# By ID
TEXT_INPUT_VIEW = 'com.bkstg:id/post_preview_text_input_view'
ADD_TEXT = 'com.bkstg:id/post_preview_caption_input_view'
MAKE_PHOTO_BUTTON = 'com.bkstg:id/post_preview_camera_button'
POST_BUTTON = 'com.bkstg:id/post_preview_send_button'

# By xpath
LAST_GALLERY_PHOTO = '//android.support.v7.widget.RecyclerView[1]/android.widget.FrameLayout[3]/android.widget.ImageView'
CAMERA_PREVIEW = '//android.support.v7.widget.RecyclerView[1]/android.widget.FrameLayout[2]/android.view.View'
MEDIA_GALLERY = '//android.support.v7.widget.RecyclerView[1]/android.widget.GridLayout'
SELECT_PHOTO = '//android.widget.ListView/android.widget.LinearLayout[1]'
SELECT_CONTACTS = '//android.widget.ListView/android.widget.LinearLayout[2]'
SELECT_MUSIC = '//android.widget.ListView/android.widget.LinearLayout[3]'
OPEN_NATIVE_PHOTO_GALLERY = '//android.support.v7.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.ImageView'
SELECT_PHOTO_ITEM_FROM_GALLERY = '//android.support.v7.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.ImageView'

# -------------------------------------Community---------------------------------
# By Name
FILTER_HOT = 'HOT'
FILTER_NEW = 'NEW'
FILTER_NEARBY = 'NEARBY'
FILTER_FOLLOWING = 'FOLLOWING'
PROMOTED_HASHTAGS = '//android.support.v4.view.ViewPager/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.view.View/android.widget.TextView[%s]'