DROP PROCEDURE ADM_04_UserRole
GO
CREATE PROCEDURE ADM_04_UserRole
                 @P_cUSR_PK NVarchar(32)

WITH ENCRYPTION AS

SET NOCOUNT ON

DECLARE @V_cROL_PK   NVarchar(16),
        @V_cROL_Date NVarchar(10),
        @V_cROL_Name NVarchar(32),
        @V_cCFG      NVarchar(1)

SELECT N'<REP Mode="Renew" Type="Vary">'+
       N'<th class="TC_AlignCM" colspan="5" id="THD_UserRole"> ：【 '+RTRIM(cUSR_PK)+N' 】'+RTRIM(cUSR_Name)+N'</th><tbody id="TBD_UserRole">'
FROM   BIS_User
WHERE  cUSR_PK = @P_cUSR_PK

DECLARE X_CUR CURSOR LOCAL FOR

SELECT cROL_PK,cROL_Name,CONVERT(Char(10),dROL_Date,120),CASE WHEN T2.cROL_FK IS NULL THEN N'' ELSE N'●' END
FROM        BIS_Role      T1
LEFT   JOIN BIS_User_Role T2 ON (T1.cROL_PK=T2.cROL_FK AND T2.cUSR_FK=@P_cUSR_PK)
ORDER  BY T1.cROL_PK

OPEN X_CUR FETCH NEXT FROM X_CUR INTO @V_cROL_PK,@V_cROL_Name,@V_cROL_Date,@V_cCFG

WHILE @@FETCH_STATUS = 0 BEGIN

      SELECT N'<tr ROL_PK="'+RTRIM(@V_cROL_PK)+N'" onclick="window.xeTR_Select(this);">'+
             N'<td class="TC_AlignCM" onclick="this.textContent=(this.textContent===''''?''●'':'''');">'+RTRIM(@V_cCFG)     +N'</td>'+
             N'<td class="TC_AlignCM">'                                                                  +RTRIM(@V_cCFG)     +N'</td>'+
             N'<td class="TC_AlignLM">'                                                                  +RTRIM(@V_cROL_PK)  +N'</td>'+
             N'<td class="TC_AlignLM TC_Icon Role">'                                                     +RTRIM(@V_cROL_Name)+N'</td>'+
             N'<td class="TC_AlignCM">'                                                                  +RTRIM(@V_cROL_Date)+N'</td></tr>'

      FETCH NEXT FROM X_CUR INTO @V_cROL_PK,@V_cROL_Name,@V_cROL_Date,@V_cCFG

END

CLOSE X_CUR DEALLOCATE X_CUR

SELECT N'</tbody>'

EXEC BIS_DesktopEdit 'CONFIG,EXPORT'

SELECT N'</REP>'

RETURN