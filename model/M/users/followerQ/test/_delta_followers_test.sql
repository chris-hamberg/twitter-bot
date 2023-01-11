INSERT INTO user (id, name, username) VALUES (0, 'Taco',  'Bell');
INSERT INTO user (id, name, username) VALUES (1, 'Bell',  'Taco');
INSERT INTO user (id, name, username) VALUES (2, 'Jim',   'Jones');
INSERT INTO user (id, name, username) VALUES (3, 'Susan', 'Sally');
INSERT INTO user (id, name, username) VALUES (4, 'Sally', 'Susan');
INSERT INTO user (id, name, username) VALUES (5, 'Blue',  'Balls');
INSERT INTO user (id, name, username) VALUES (6, 'Kyle',  'Marsh');
INSERT INTO user (id, name, username) VALUES (7, 'Stan',  'Marsh');
INSERT INTO user (id, name, username) VALUES (8, 'Eric',  'Cartman');


INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',   0);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',  1);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',   2);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',  2);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',   3);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',  3);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',  3);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',   4);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',  4);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',  4);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'blacklist',  4);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',   5);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'blacklist',  5);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',  6);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',  6);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'blacklist',  6);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',  7);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',  7);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'blacklist',  7);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',  8);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',  8);


INSERT INTO user_s (admin, id) VALUES (12345, 0);
INSERT INTO user_s (admin, id) VALUES (12345, 1);
INSERT INTO user_s (admin, id) VALUES (12345, 2);
INSERT INTO user_s (admin, id) VALUES (12345, 3);
INSERT INTO user_s (admin, id, unfollowed_count) VALUES (12345, 4, 1);
INSERT INTO user_s (admin, id, unfollowed_count) VALUES (12345, 5, 3);
INSERT INTO user_s (admin, id, unfollowed_count) VALUES (12345, 6, 1);
INSERT INTO user_s (admin, id, unfollowed_count) VALUES (12345, 7, 3);
INSERT INTO user_s (admin, id) VALUES (12345, 8);
