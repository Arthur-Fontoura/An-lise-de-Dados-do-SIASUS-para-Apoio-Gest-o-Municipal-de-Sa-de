USE dbsia;

DROP VIEW IF EXISTS pa_ijui;

CREATE OR REPLACE VIEW pa_ijui AS
SELECT
    -- 1. DIMENSÃO TEMPORAL
    dt.ano AS Ano,
    dt.mes AS Mes,
    dt.anobi AS AnoBimestre,
    dt.anotri AS AnoTrimestre,
    -- 2. ESTABELECIMENTO DE SAÚDE
    ca.fantasia AS Estabelecimento,
    -- 3. PROCEDIMENTO AMBULATORIAL
    pro.ip_dscr AS Procedimento,
    -- 4. OCUPAÇÃO PROFISSIONAL
    cb.ds_cbo AS Ocupacao,
    -- 5. PERFIL DEMOGRÁFICO
    pa.pa_sexo,
    pa.pa_idade,
    -- 6. DIAGNÓSTICO PRINCIPAL
    pa.pa_cidpri,
    cid.cd_descr AS Diagnostico,
    -- 7. MUNICÍPIO DO ESTABELECIMENTO
    mun_est.ds_nome AS MunicipioEstabelecimento,
    -- 8. MUNICÍPIO DO PACIENTE
    mun_pac.ds_nome AS MunicipioPaciente,
    -- 9. PRODUÇÃO AMBULATORIAL
    pa.pa_qtdpro,
    pa.pa_qtdapr,
    -- 10. VALORES FINANCEIROS
    pa.pa_valpro,
    pa.pa_valapr
FROM pars AS pa
LEFT JOIN cadgerrs AS ca
    ON pa.pa_coduni = ca.cnes
LEFT JOIN procedimentos AS pro
    ON pa.pa_proc_id = pro.ip_cod
LEFT JOIN cbo AS cb
    ON pa.pa_cbocod = cb.cbo
LEFT JOIN cid
    ON pa.pa_cidpri = cid.cd_cod
LEFT JOIN tb_municip AS mun_est
    ON pa.pa_ufmun = mun_est.co_municip
LEFT JOIN tb_municip AS mun_pac
    ON pa.pa_munpcn = mun_pac.co_municip
LEFT JOIN DIMTEMPO AS dt
    ON pa.pa_mvm = dt.anomes
WHERE pa.pa_ufmun = '431020';

SELECT COUNT(*) FROM pa_ijui;
SELECT * FROM pa_ijui LIMIT 5;
