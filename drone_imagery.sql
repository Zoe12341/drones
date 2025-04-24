--
-- PostgreSQL database dump
--

-- Dumped from database version 14.16 (Homebrew)
-- Dumped by pg_dump version 17.4 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: sonorahalili
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO sonorahalili;

--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: files; Type: TABLE; Schema: public; Owner: sonorahalili
--

CREATE TABLE public.files (
    file_id integer NOT NULL,
    flight_id integer,
    file_name character varying(255) NOT NULL,
    file_path character varying(255) NOT NULL,
    file_type character varying(20)
);


ALTER TABLE public.files OWNER TO sonorahalili;

--
-- Name: files_file_id_seq; Type: SEQUENCE; Schema: public; Owner: sonorahalili
--

CREATE SEQUENCE public.files_file_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.files_file_id_seq OWNER TO sonorahalili;

--
-- Name: files_file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sonorahalili
--

ALTER SEQUENCE public.files_file_id_seq OWNED BY public.files.file_id;


--
-- Name: flights; Type: TABLE; Schema: public; Owner: sonorahalili
--

CREATE TABLE public.flights (
    flight_id integer NOT NULL,
    project_id integer,
    flight_date date NOT NULL,
    folder_path character varying(255) NOT NULL
);


ALTER TABLE public.flights OWNER TO sonorahalili;

--
-- Name: flights_flight_id_seq; Type: SEQUENCE; Schema: public; Owner: sonorahalili
--

CREATE SEQUENCE public.flights_flight_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.flights_flight_id_seq OWNER TO sonorahalili;

--
-- Name: flights_flight_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sonorahalili
--

ALTER SEQUENCE public.flights_flight_id_seq OWNED BY public.flights.flight_id;


--
-- Name: personal; Type: TABLE; Schema: public; Owner: sonorahalili
--

CREATE TABLE public.personal (
    id integer NOT NULL,
    name character varying(100),
    date timestamp without time zone,
    filepath text
);


ALTER TABLE public.personal OWNER TO sonorahalili;

--
-- Name: personal_id_seq; Type: SEQUENCE; Schema: public; Owner: sonorahalili
--

CREATE SEQUENCE public.personal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.personal_id_seq OWNER TO sonorahalili;

--
-- Name: personal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sonorahalili
--

ALTER SEQUENCE public.personal_id_seq OWNED BY public.personal.id;


--
-- Name: personal_imagery; Type: TABLE; Schema: public; Owner: sonorahalili
--

CREATE TABLE public.personal_imagery (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    capture_date date NOT NULL,
    location character varying(255),
    file_path character varying(512) NOT NULL,
    owner character varying(255),
    tags character varying(255)[]
);


ALTER TABLE public.personal_imagery OWNER TO sonorahalili;

--
-- Name: personal_imagery_id_seq; Type: SEQUENCE; Schema: public; Owner: sonorahalili
--

CREATE SEQUENCE public.personal_imagery_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.personal_imagery_id_seq OWNER TO sonorahalili;

--
-- Name: personal_imagery_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sonorahalili
--

ALTER SEQUENCE public.personal_imagery_id_seq OWNED BY public.personal_imagery.id;


--
-- Name: professional; Type: TABLE; Schema: public; Owner: sonorahalili
--

CREATE TABLE public.professional (
    id integer NOT NULL,
    name character varying(100),
    date timestamp without time zone,
    filepath text
);


ALTER TABLE public.professional OWNER TO sonorahalili;

--
-- Name: professional_old; Type: TABLE; Schema: public; Owner: sonorahalili
--

CREATE TABLE public.professional_old (
    id integer NOT NULL,
    name character varying(100),
    date timestamp without time zone,
    filepath text
);


ALTER TABLE public.professional_old OWNER TO sonorahalili;

--
-- Name: professional_id_seq; Type: SEQUENCE; Schema: public; Owner: sonorahalili
--

CREATE SEQUENCE public.professional_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.professional_id_seq OWNER TO sonorahalili;

--
-- Name: professional_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sonorahalili
--

ALTER SEQUENCE public.professional_id_seq OWNED BY public.professional_old.id;


--
-- Name: professional_id_seq1; Type: SEQUENCE; Schema: public; Owner: sonorahalili
--

CREATE SEQUENCE public.professional_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.professional_id_seq1 OWNER TO sonorahalili;

--
-- Name: professional_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: sonorahalili
--

ALTER SEQUENCE public.professional_id_seq1 OWNED BY public.professional.id;


--
-- Name: professional_imagery; Type: TABLE; Schema: public; Owner: sonorahalili
--

CREATE TABLE public.professional_imagery (
    id integer NOT NULL,
    name character varying(255),
    capture_date date,
    file_path text,
    location character varying(255),
    flight_operator character varying(255),
    project_name character varying(255),
    resolution character varying(50)
);


ALTER TABLE public.professional_imagery OWNER TO sonorahalili;

--
-- Name: professional_imagery_id_seq; Type: SEQUENCE; Schema: public; Owner: sonorahalili
--

CREATE SEQUENCE public.professional_imagery_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.professional_imagery_id_seq OWNER TO sonorahalili;

--
-- Name: professional_imagery_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sonorahalili
--

ALTER SEQUENCE public.professional_imagery_id_seq OWNED BY public.professional_imagery.id;


--
-- Name: projects; Type: TABLE; Schema: public; Owner: sonorahalili
--

CREATE TABLE public.projects (
    project_id integer NOT NULL,
    project_name character varying(100) NOT NULL
);


ALTER TABLE public.projects OWNER TO sonorahalili;

--
-- Name: projects_project_id_seq; Type: SEQUENCE; Schema: public; Owner: sonorahalili
--

CREATE SEQUENCE public.projects_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.projects_project_id_seq OWNER TO sonorahalili;

--
-- Name: projects_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sonorahalili
--

ALTER SEQUENCE public.projects_project_id_seq OWNED BY public.projects.project_id;


--
-- Name: test; Type: TABLE; Schema: public; Owner: sonorahalili
--

CREATE TABLE public.test (
    id integer NOT NULL
);


ALTER TABLE public.test OWNER TO sonorahalili;

--
-- Name: test_id_seq; Type: SEQUENCE; Schema: public; Owner: sonorahalili
--

CREATE SEQUENCE public.test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.test_id_seq OWNER TO sonorahalili;

--
-- Name: test_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sonorahalili
--

ALTER SEQUENCE public.test_id_seq OWNED BY public.test.id;


--
-- Name: files file_id; Type: DEFAULT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.files ALTER COLUMN file_id SET DEFAULT nextval('public.files_file_id_seq'::regclass);


--
-- Name: flights flight_id; Type: DEFAULT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.flights ALTER COLUMN flight_id SET DEFAULT nextval('public.flights_flight_id_seq'::regclass);


--
-- Name: personal id; Type: DEFAULT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.personal ALTER COLUMN id SET DEFAULT nextval('public.personal_id_seq'::regclass);


--
-- Name: personal_imagery id; Type: DEFAULT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.personal_imagery ALTER COLUMN id SET DEFAULT nextval('public.personal_imagery_id_seq'::regclass);


--
-- Name: professional id; Type: DEFAULT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.professional ALTER COLUMN id SET DEFAULT nextval('public.professional_id_seq1'::regclass);


--
-- Name: professional_imagery id; Type: DEFAULT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.professional_imagery ALTER COLUMN id SET DEFAULT nextval('public.professional_imagery_id_seq'::regclass);


--
-- Name: professional_old id; Type: DEFAULT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.professional_old ALTER COLUMN id SET DEFAULT nextval('public.professional_id_seq'::regclass);


--
-- Name: projects project_id; Type: DEFAULT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.projects ALTER COLUMN project_id SET DEFAULT nextval('public.projects_project_id_seq'::regclass);


--
-- Name: test id; Type: DEFAULT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.test ALTER COLUMN id SET DEFAULT nextval('public.test_id_seq'::regclass);


--
-- Data for Name: files; Type: TABLE DATA; Schema: public; Owner: sonorahalili
--

COPY public.files (file_id, flight_id, file_name, file_path, file_type) FROM stdin;
\.


--
-- Data for Name: flights; Type: TABLE DATA; Schema: public; Owner: sonorahalili
--

COPY public.flights (flight_id, project_id, flight_date, folder_path) FROM stdin;
\.


--
-- Data for Name: personal; Type: TABLE DATA; Schema: public; Owner: sonorahalili
--

COPY public.personal (id, name, date, filepath) FROM stdin;
1	10.23Bahamas2020Exports	2020-10-23 00:00:00	/Users/sonorahalili/Desktop/drones/data/10.23Bahamas2020Exports
\.


--
-- Data for Name: personal_imagery; Type: TABLE DATA; Schema: public; Owner: sonorahalili
--

COPY public.personal_imagery (id, name, capture_date, location, file_path, owner, tags) FROM stdin;
1	Family_Picnic	2023-08-10	Local Beach	/drones/personal/summer_2023.jpg	Alice	{summer,family}
2	Sunset_Flight	2023-09-05	Mountains	/drones/personal/sunset_drone.jpg	Bob	{nature,sunset}
\.


--
-- Data for Name: professional; Type: TABLE DATA; Schema: public; Owner: sonorahalili
--

COPY public.professional (id, name, date, filepath) FROM stdin;
1	DJI_202410111314_010_ParadisePondBaseWithLeg 2	2024-10-11 13:14:00	/Users/sonorahalili/Desktop/drones/data/DJI_202410111314_010_ParadisePondBaseWithLeg 2
2	DJI_202410111314_010_ParadisePondBaseWithLeg	2024-10-11 13:14:00	/Users/sonorahalili/Desktop/drones/data/DJI_202410111314_010_ParadisePondBaseWithLeg
\.


--
-- Data for Name: professional_imagery; Type: TABLE DATA; Schema: public; Owner: sonorahalili
--

COPY public.professional_imagery (id, name, capture_date, file_path, location, flight_operator, project_name, resolution) FROM stdin;
1	DJI_202410111314_010_ParadisePondBaseWithLeg 2	2024-10-11	/Users/sonorahalili/Desktop/drones/data/DJI_202410111314_010_ParadisePondBaseWithLeg 2	\N	\N	\N	\N
2	DJI_202410111314_010_ParadisePondBaseWithLeg	2024-10-11	/Users/sonorahalili/Desktop/drones/data/DJI_202410111314_010_ParadisePondBaseWithLeg	\N	\N	\N	\N
\.


--
-- Data for Name: professional_old; Type: TABLE DATA; Schema: public; Owner: sonorahalili
--

COPY public.professional_old (id, name, date, filepath) FROM stdin;
1	DJI_202410111314_010_ParadisePondBaseWithLeg 2	2024-10-11 13:14:00	/Users/sonorahalili/Desktop/drones/data/DJI_202410111314_010_ParadisePondBaseWithLeg 2
2	DJI_202410111314_010_ParadisePondBaseWithLeg	2024-10-11 13:14:00	/Users/sonorahalili/Desktop/drones/data/DJI_202410111314_010_ParadisePondBaseWithLeg
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: sonorahalili
--

COPY public.projects (project_id, project_name) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: sonorahalili
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: test; Type: TABLE DATA; Schema: public; Owner: sonorahalili
--

COPY public.test (id) FROM stdin;
\.


--
-- Name: files_file_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sonorahalili
--

SELECT pg_catalog.setval('public.files_file_id_seq', 1, false);


--
-- Name: flights_flight_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sonorahalili
--

SELECT pg_catalog.setval('public.flights_flight_id_seq', 1, false);


--
-- Name: personal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sonorahalili
--

SELECT pg_catalog.setval('public.personal_id_seq', 1, true);


--
-- Name: personal_imagery_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sonorahalili
--

SELECT pg_catalog.setval('public.personal_imagery_id_seq', 2, true);


--
-- Name: professional_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sonorahalili
--

SELECT pg_catalog.setval('public.professional_id_seq', 2, true);


--
-- Name: professional_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: sonorahalili
--

SELECT pg_catalog.setval('public.professional_id_seq1', 2, true);


--
-- Name: professional_imagery_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sonorahalili
--

SELECT pg_catalog.setval('public.professional_imagery_id_seq', 4, true);


--
-- Name: projects_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sonorahalili
--

SELECT pg_catalog.setval('public.projects_project_id_seq', 1, false);


--
-- Name: test_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sonorahalili
--

SELECT pg_catalog.setval('public.test_id_seq', 1, false);


--
-- Name: files files_pkey; Type: CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (file_id);


--
-- Name: flights flights_pkey; Type: CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.flights
    ADD CONSTRAINT flights_pkey PRIMARY KEY (flight_id);


--
-- Name: personal_imagery personal_imagery_pkey; Type: CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.personal_imagery
    ADD CONSTRAINT personal_imagery_pkey PRIMARY KEY (id);


--
-- Name: personal personal_pkey; Type: CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.personal
    ADD CONSTRAINT personal_pkey PRIMARY KEY (id);


--
-- Name: professional_imagery professional_imagery_file_path_key; Type: CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.professional_imagery
    ADD CONSTRAINT professional_imagery_file_path_key UNIQUE (file_path);


--
-- Name: professional_imagery professional_imagery_pkey; Type: CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.professional_imagery
    ADD CONSTRAINT professional_imagery_pkey PRIMARY KEY (id);


--
-- Name: professional_old professional_pkey; Type: CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.professional_old
    ADD CONSTRAINT professional_pkey PRIMARY KEY (id);


--
-- Name: professional professional_pkey1; Type: CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.professional
    ADD CONSTRAINT professional_pkey1 PRIMARY KEY (id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (project_id);


--
-- Name: test test_pkey; Type: CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.test
    ADD CONSTRAINT test_pkey PRIMARY KEY (id);


--
-- Name: idx_personal_date; Type: INDEX; Schema: public; Owner: sonorahalili
--

CREATE INDEX idx_personal_date ON public.personal_imagery USING btree (capture_date);


--
-- Name: idx_professional_date; Type: INDEX; Schema: public; Owner: sonorahalili
--

CREATE INDEX idx_professional_date ON public.professional_imagery USING btree (capture_date);


--
-- Name: files files_flight_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_flight_id_fkey FOREIGN KEY (flight_id) REFERENCES public.flights(flight_id);


--
-- Name: flights flights_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sonorahalili
--

ALTER TABLE ONLY public.flights
    ADD CONSTRAINT flights_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(project_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: sonorahalili
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

