export const FEED = '/feed'
export const LOGIN = '/login';
export const DESK = '/desk';
export const REGISTER = '/register';
export const CREATE_POEM = '/create-poem';

// Backend routes
export const API_LOGIN = '/login';
export const API_REGISTER = '/register';
export const API_POEMS = '/poems';
export const API_MY_POEMS = '/my/poems';
export const API_COMMENTS = '/comments';
export const API_LIKES = '/likes';


export default {
    PRIVATE_ROUTES: [DESK, FEED, CREATE_POEM],
    PUBLIC_ROUTES: [LOGIN, REGISTER],
}
