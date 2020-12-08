SET timezone ='+3';

create table Advertisement
(
    ADD_ID SERIAL PRIMARY KEY,
    search_string TEXT NOT NULL,
    region int not null,
    UNIQUE (search_string, region)
);

create table AdvertisementCounter
(
    ID serial not null primary key,
    ADD_ID int REFERENCES Advertisement(ADD_ID),
    ADD_NUM int default 0,
    ADD_TOP jsonb,
    TIME_STAMP timestamp default now()
);

create index idx_add_table on AdvertisementCounter(ADD_ID,ADD_NUM,time_stamp);
create index idx_add_top_table on AdvertisementCounter(ADD_ID,ADD_TOP,time_stamp);