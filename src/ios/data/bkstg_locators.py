#  -------------------------------------Auth Page--------------------------------------
# By Name
LOG_IN_BUTTON = 'LOG IN'
SIGN_IN_BUTTON = 'Log in'
EMAIL_BUTTON = 'EMAIL'
SIGN_UP_BUTTON = 'SIGN UP'
AUTH_NEXT_BUTTON = 'NEXT'
NOTIFICATION_OK_BUTTON = 'OK'
NOTIFY_ME_BUTTON = 'NOTIFY ME'
# XPath
EMAIL_FIELD = '//UIATextField[@value="EMAIL"]'
CREATE_PASSWORD_FIELD = '//UIASecureTextField[@value="CREATE PASSWORD"]'
PASSWORD_FIELD = '//UIASecureTextField[@value="PASSWORD"]'
NICKNAME_FIELD = '//UIATextField[@value="NICKNAME"]'
USERNAME_FIELD = '//UIATextField[@value="FIRST & LASTNAME"]'
ARTIST_MODE_SWITCH = '//UIAApplication[1]/UIAWindow[1]/UIASwitch[1]'


#  -------------------------------------Cards Navigation Page--------------------------------------
# Name
# ADD_HUB_BUTTON = 'add hub icon'
#DELETE_HUB_BUTTON = 'delete hub btn'

# Xpath
SEARCH_FIELD = '//UIAApplication[1]/UIAWindow[1]/UIATextField[1]'
ADD_HUB_BUTTON = '//UIACollectionCell[@name="%s"]/UIAButton[@name="add hub icon"]'
CARD_TITLE = '//UIAApplication[1]/UIAWindow[1]/UIACollectionView[2]/UIACollectionCell[3]/UIAStaticText[1]'
DELETE_HUB_BUTTON = '//UIAApplication[1]/UIAWindow[1]/UIAButton[3]'
GHOST_CARD_NOTIFY_BUTTON = '//UIAButton[@name="Notify me"]'
CARD_LAYOUT = '//UIAApplication[1]/UIAWindow[1]/UIACollectionView[2]/UIACollectionCell[2]'

#  -------------------------------------Hub Page----------------------------------------------------
# Xpath
ADD_COMMENT_BUTTON = '//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[2]'
#LIKES_COUNTER = '//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAStaticText[3]'
LIKES_COUNTER = '//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAStaticText[5]'
COMMENT_FIELD = '//UIAApplication[1]/UIAWindow[1]/UIAToolbar[1]/UIATextView[1]'
POST_COMMENT_BUTTON = '//UIAApplication[1]/UIAWindow[1]/UIAToolbar[1]/UIAButton[4]'
COMMENT_TEXT = '//UIAStaticText[@value="%s"]'
CLOSE_COMMENTS_BUTTON = '//UIAApplication[1]/UIAWindow[1]/UIAButton[1]'
LIKE_BUTTON = '//*[@name="likeHeartView"]'
NO_LIKES_TITLE = '//UIAScrollView[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAStaticText[@value="NO LIKES YET. BE #1"]'
HUB_ARTIST_TITLE = '//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIAStaticText[1]'
NO_LIKES_VIEW = '//UIAApplication[1]/UIAWindow[1]/UIAScrollView[1]/UIACollectionView[1]/UIACollectionCell[1]/UIACollectionView[1]'
CREATION_TOOLS_BUTTON = '//UIAApplication[1]/UIAWindow[1]/UIAButton[3]'
# By Name
BKSTG_BUTTON = 'menu_bkstg_pan_icon'
BKSTG_FEED_BUTTON = 'FEED'
BKSTG_COMMUNITY_BUTTON = 'COMMUNITY'
BKSTG_PICTURES_BUTTON = 'PICTURES'

#  -------------------------------------Creation Tools Page----------------------------------------------------
