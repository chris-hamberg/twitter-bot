--follower
--following
--following,follower

--follower,type_alpha,expired
--follower,type_alpha,not expired
--following,type_alpha,expired
--following,type_alpha,not expired
--following,follower,type_alpha,expired
--following,follower,type_alpha,not expired

--type_alpha,expired
--type_alpha,not expired
--type_alpha,unfriendQ,expired
--type_alpha,unfriendQ,not expired

--unfriendQ
--follower,unfriendQ
--following,unfriendQ
--following,follower, unfriendQ

--follower,unfriendQ,type_alpha,expired
--follower,unfriendQ,type_alpha,not expired
--following,unfriendQ,type_alpha,expired
--following,unfriendQ,type_alpha,not expired
--follower,following,type_alpha,expired
--follower,following,type_alpha,not expired


INSERT INTO user (id, name, username) VALUES (0,  'Taco',    'Bell');
INSERT INTO user (id, name, username) VALUES (1,  'Bill',    'Dollar');
INSERT INTO user (id, name, username) VALUES (2,  'Ted',     'Simons');
INSERT INTO user (id, name, username) VALUES (3,  'Darth',   'Maul');
INSERT INTO user (id, name, username) VALUES (4,  'Pizza',   'Hut');
INSERT INTO user (id, name, username) VALUES (5,  'Elon',    'Musk');
INSERT INTO user (id, name, username) VALUES (6,  'T',       'B');
INSERT INTO user (id, name, username) VALUES (7,  'B',       'D');
INSERT INTO user (id, name, username) VALUES (8,  'T',       'S');
INSERT INTO user (id, name, username) VALUES (9,  'D',       'M');
INSERT INTO user (id, name, username) VALUES (10, 'P',       'H');
INSERT INTO user (id, name, username) VALUES (11, 'E',       'M');
INSERT INTO user (id, name, username) VALUES (12, 'Burr',    'Bell');
INSERT INTO user (id, name, username) VALUES (13, 'Buritto', 'Dollar');
INSERT INTO user (id, name, username) VALUES (14, 'Ted',     'Pizza');
INSERT INTO user (id, name, username) VALUES (15, 'Darth',   'Bear');
INSERT INTO user (id, name, username) VALUES (16, 'Grass',   'Hut');
INSERT INTO user (id, name, username) VALUES (17, 'Brandon', 'Musk');
INSERT INTO user (id, name, username) VALUES (18, 'Simon',   'Butts');
INSERT INTO user (id, name, username) VALUES (19, 'Jim',     'Nickle');
INSERT INTO user (id, name, username) VALUES (20, 'Big',     'Bird');
INSERT INTO user (id, name, username) VALUES (21, 'Garth',   'Wayne');
INSERT INTO user (id, name, username) VALUES (22, 'Bruce',   'Batman');


INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',    0);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',     1);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',    2);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',     2);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',    3);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',      3);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',    4);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',      4);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',     5);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',      5);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',     6);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',      6);


INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',    7);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',     7);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',      7);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',    8);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',     8);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',      8);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',      9);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',     10);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',     11);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   11);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',     12);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   12);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   13);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',   14);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   14);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',    15);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   15);


INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',    16);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',   16);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   16);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',   17);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   17);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',     17);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',   18);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   18);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',     18);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',    19);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   19);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',     19);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',    20);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   20);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',     20);

INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',   21);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',    21);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   21);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',     21);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'following',   22);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'follower',    22);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'unfriendQ',   22);
INSERT INTO user_c (admin, cat, id) VALUES (12345, 'type_alpha',     22);


INSERT INTO type_alpha (admin, id, following) VALUES (12345, 3, True);
INSERT INTO type_alpha (admin, id, following) VALUES (12345, 4, True);
INSERT INTO type_alpha (admin, id) VALUES (12345, 5);
INSERT INTO type_alpha (admin, id) VALUES (12345, 6);
INSERT INTO type_alpha (admin, id, following) VALUES (12345, 7, True);
INSERT INTO type_alpha (admin, id, following) VALUES (12345, 8, True);
INSERT INTO type_alpha (admin, id) VALUES (12345, 9);
INSERT INTO type_alpha (admin, id) VALUES (12345, 10);
INSERT INTO type_alpha (admin, id) VALUES (12345, 11);
INSERT INTO type_alpha (admin, id) VALUES (12345, 12);
INSERT INTO type_alpha (admin, id, following) VALUES (12345, 17, True);
INSERT INTO type_alpha (admin, id, following) VALUES (12345, 18, True);
INSERT INTO type_alpha (admin, id) VALUES (12345, 19);
INSERT INTO type_alpha (admin, id) VALUES (12345, 20);
INSERT INTO type_alpha (admin, id, following) VALUES (12345, 21, True);
INSERT INTO type_alpha (admin, id, following) VALUES (12345, 22, True);


INSERT INTO user_s (admin, id) VALUES (12345, 0);
INSERT INTO user_s (admin, id) VALUES (12345, 1);
INSERT INTO user_s (admin, id) VALUES (12345, 2);
INSERT INTO user_s (admin, id) VALUES (12345, 3);
INSERT INTO user_s (admin, id) VALUES (12345, 4);
INSERT INTO user_s (admin, id) VALUES (12345, 5);
INSERT INTO user_s (admin, id) VALUES (12345, 6);
INSERT INTO user_s (admin, id) VALUES (12345, 7);
INSERT INTO user_s (admin, id) VALUES (12345, 8);
INSERT INTO user_s (admin, id) VALUES (12345, 9);
INSERT INTO user_s (admin, id) VALUES (12345, 10);
INSERT INTO user_s (admin, id) VALUES (12345, 11);
INSERT INTO user_s (admin, id) VALUES (12345, 12);
INSERT INTO user_s (admin, id) VALUES (12345, 13);
INSERT INTO user_s (admin, id) VALUES (12345, 14);
INSERT INTO user_s (admin, id) VALUES (12345, 15);
INSERT INTO user_s (admin, id) VALUES (12345, 16);
INSERT INTO user_s (admin, id) VALUES (12345, 17);
INSERT INTO user_s (admin, id) VALUES (12345, 18);
INSERT INTO user_s (admin, id) VALUES (12345, 19);
INSERT INTO user_s (admin, id) VALUES (12345, 20);
INSERT INTO user_s (admin, id) VALUES (12345, 21);
INSERT INTO user_s (admin, id) VALUES (12345, 22);
