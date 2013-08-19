--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE USER 'icecast';
CREATE DATABASE 'icecast_log' ENCODING 'UTF-8' TEMPLATE template0 LC_COLLATE 'en_GB.utf8' LC_CTYPE 'en_GB.utf8';

--
-- Name: log; Type: TABLE; Schema: public; Owner: icecast; Tablespace: 
--

CREATE TABLE log (
    id integer NOT NULL,
    ip inet NOT NULL,
    "timestamp" timestamp with time zone DEFAULT now() NOT NULL,
    mount_point_id integer NOT NULL,
    user_agent_id integer NOT NULL,
    referer_id integer NOT NULL,
    bytes bigint NOT NULL
);


ALTER TABLE public.log OWNER TO icecast;

--
-- Name: mount_points; Type: TABLE; Schema: public; Owner: icecast; Tablespace: 
--

CREATE TABLE mount_points (
    id integer NOT NULL,
    mount_point character varying NOT NULL,
    bitrate integer NOT NULL,
    date_added timestamp with time zone DEFAULT now() NOT NULL,
    date_retired timestamp with time zone,
    count boolean DEFAULT true NOT NULL
);


ALTER TABLE public.mount_points OWNER TO icecast;

--
-- Name: referers; Type: TABLE; Schema: public; Owner: icecast; Tablespace: 
--

CREATE TABLE referers (
    id integer NOT NULL,
    url character varying
);


ALTER TABLE public.referers OWNER TO icecast;

--
-- Name: user_agents; Type: TABLE; Schema: public; Owner: icecast; Tablespace: 
--

CREATE TABLE user_agents (
    id integer NOT NULL,
    ua_string character varying
);


ALTER TABLE public.user_agents OWNER TO icecast;

--
-- Name: combined_log; Type: VIEW; Schema: public; Owner: icecast
--

CREATE VIEW combined_log AS
    SELECT log.id, log.ip, log."timestamp", mount_points.mount_point, mount_points.bitrate, user_agents.ua_string, referers.url, log.bytes FROM (((log JOIN mount_points ON ((log.mount_point_id = mount_points.id))) JOIN user_agents ON ((log.user_agent_id = user_agents.id))) JOIN referers ON ((log.referer_id = referers.id))) ORDER BY log.id;


ALTER TABLE public.combined_log OWNER TO icecast;

--
-- Name: listener_hours; Type: VIEW; Schema: public; Owner: icecast
--

CREATE VIEW listener_hours AS
    SELECT mount_points.mount_point, max(log."timestamp") AS max_timestamp, min(log."timestamp") AS min_timestamp, round((((sum(log.bytes) / (1024)::numeric) / (max(mount_points.bitrate))::numeric) / ((60 * 60))::numeric), 2) AS listener_hours FROM (log JOIN mount_points ON ((log.mount_point_id = mount_points.id))) WHERE (mount_points.count = true) GROUP BY mount_points.mount_point;


ALTER TABLE public.listener_hours OWNER TO icecast;

--
-- Name: log_id_seq; Type: SEQUENCE; Schema: public; Owner: icecast
--

CREATE SEQUENCE log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.log_id_seq OWNER TO icecast;

--
-- Name: log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: icecast
--

ALTER SEQUENCE log_id_seq OWNED BY log.id;


--
-- Name: mount_points_id_seq; Type: SEQUENCE; Schema: public; Owner: icecast
--

CREATE SEQUENCE mount_points_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.mount_points_id_seq OWNER TO icecast;

--
-- Name: mount_points_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: icecast
--

ALTER SEQUENCE mount_points_id_seq OWNED BY mount_points.id;


--
-- Name: referers_id_seq; Type: SEQUENCE; Schema: public; Owner: icecast
--

CREATE SEQUENCE referers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.referers_id_seq OWNER TO icecast;

--
-- Name: referers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: icecast
--

ALTER SEQUENCE referers_id_seq OWNED BY referers.id;


--
-- Name: user_agents_id_seq; Type: SEQUENCE; Schema: public; Owner: icecast
--

CREATE SEQUENCE user_agents_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.user_agents_id_seq OWNER TO icecast;

--
-- Name: user_agents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: icecast
--

ALTER SEQUENCE user_agents_id_seq OWNED BY user_agents.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: icecast
--

ALTER TABLE ONLY log ALTER COLUMN id SET DEFAULT nextval('log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: icecast
--

ALTER TABLE ONLY mount_points ALTER COLUMN id SET DEFAULT nextval('mount_points_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: icecast
--

ALTER TABLE ONLY referers ALTER COLUMN id SET DEFAULT nextval('referers_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: icecast
--

ALTER TABLE ONLY user_agents ALTER COLUMN id SET DEFAULT nextval('user_agents_id_seq'::regclass);


--
-- Name: log_pkey; Type: CONSTRAINT; Schema: public; Owner: icecast; Tablespace: 
--

ALTER TABLE ONLY log
    ADD CONSTRAINT log_pkey PRIMARY KEY (id);


--
-- Name: mount_points_pkey; Type: CONSTRAINT; Schema: public; Owner: icecast; Tablespace: 
--

ALTER TABLE ONLY mount_points
    ADD CONSTRAINT mount_points_pkey PRIMARY KEY (id);


--
-- Name: referers_pkey; Type: CONSTRAINT; Schema: public; Owner: icecast; Tablespace: 
--

ALTER TABLE ONLY referers
    ADD CONSTRAINT referers_pkey PRIMARY KEY (id);


--
-- Name: user_agents_pkey; Type: CONSTRAINT; Schema: public; Owner: icecast; Tablespace: 
--

ALTER TABLE ONLY user_agents
    ADD CONSTRAINT user_agents_pkey PRIMARY KEY (id);


--
-- Name: log_fkey_mount_points; Type: FK CONSTRAINT; Schema: public; Owner: icecast
--

ALTER TABLE ONLY log
    ADD CONSTRAINT log_fkey_mount_points FOREIGN KEY (mount_point_id) REFERENCES mount_points(id);


--
-- Name: log_fkey_referers; Type: FK CONSTRAINT; Schema: public; Owner: icecast
--

ALTER TABLE ONLY log
    ADD CONSTRAINT log_fkey_referers FOREIGN KEY (referer_id) REFERENCES referers(id);


--
-- Name: log_fkey_user_agents; Type: FK CONSTRAINT; Schema: public; Owner: icecast
--

ALTER TABLE ONLY log
    ADD CONSTRAINT log_fkey_user_agents FOREIGN KEY (user_agent_id) REFERENCES user_agents(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;
GRANT ALL ON SCHEMA public TO icecast;


--
-- PostgreSQL database dump complete
--
