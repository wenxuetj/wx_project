/**水务局对接脚本**/
DROP TABLE IF EXISTS `to_river_r`;
CREATE TABLE `to_river_r` (
  `stcd` varchar(20) NOT NULL,
  `tm` datetime NOT NULL,
  `systm` datetime NOT NULL,
  `z` float,
  `wptn` varchar(2),
  `wptn_name` varchar(20)
);

DROP TABLE IF EXISTS `to_rsvr_r`;
CREATE TABLE `to_rsvr_r` (
  `stcd` varchar(20) NOT NULL,
  `tm` datetime NOT NULL,
  `systm` datetime NOT NULL,
  `rz` float
);

DROP TABLE IF EXISTS `to_rain_r`;
CREATE TABLE `to_mi_rain_r` (
  `stcd` varchar(20) NOT NULL,
  `tm` datetime NOT NULL,
  `systm` datetime NOT NULL,
  `drp` float
);

DROP TABLE IF EXISTS `to_st_stbprp_b`;
CREATE TABLE `to_st_stbprp_b` (
  `stcd` varchar(20) NOT NULL,
  `stnm` varchar(50) NOT NULL,
  `lgtd` DOUBLE,
  `lttd` DOUBLE,
  `stlc` varchar(100),
  `addvcd` varchar(100),
  `sttp` varchar(100)
);