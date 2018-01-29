#!/bin/sh

Incap_File="/root/.incap.json"
curl -d api_id=23304 -d api_key=4088fa23-c869-46ad-994b-3771cdf76f08 -d page_size=200 https://my.incapsula.com/api/prov/v1/sites/list > $Incap_File
#curl -d "api_id=23304&api_key=4088fa23-c869-46ad-994b-3771cdf76f08&page_size=200" https://my.incapsula.com/api/prov/v1/sites/list
sed -i -e 's/,/\n/g ; s/:/ /g ; s/"//g' $Incap_File
Incap_Line=$(awk 'END {print NR}' $Incap_File)

###如果incap api出问题，会少于100行，退出
[ ${Incap_Line} -lt 100 ] && exit 1
Incap_Html_Tmp="/root/.incap.html.tmp"
Incap_Html="/usr/local/openresty/nginx/html/incap.html"
echo "
<html>
 <head>
  <STYLE type=text/css> 
   A {COLOR: #009933; TEXT-DECORATION: underline=none} 
   body{padding:0; margin:0;  repeat-x; font:12px Arial; }
   td{border-left:1px solid #009933;border-top:1px solid #009933;}
   img {border:0}
   table{border-right:1px solid #009933;border-bottom:1px solid #009933;margin-left:20px;}
  </STYLE>
 </head>
 <title>incap info</title>
 <body>
  <Bold><font color='RED'>最后一次更新时间 Start at: $(date '+%F %T') AMT; End at: End_Time</font></Bold>
  <br>
  <table>
   <tr>
    <th>客户名称</th>
    <th>是否Incap</th>
    <th>源服务器名称</th>
    <th>源服务器IP</th>
    <th>http域名总数</th>
    <th>https域名总数</th>
    <th>证书首域名</th>
    <th>证书包含域名数</th>
    <th>证书签发日期时间</th>
    <th>证书到期日期</th>
    <th>证书剩余天数</th>
    <th>site_name</th>
    <th>site_id</th>
    <th>incap_cname</th>
   </tr>" > ${Incap_Html_Tmp}

cd /usr/local/openresty/nginx/conf/tw_xjproxy
### 遍历现金网配置文件
for i in `ls *.conf`
do
{
    ### 现金网
    Client_Name=$(echo $i | sed 's/^xj//;s/\.conf//')
    ### 现金网http的裸域名个数统计
    Http_Count=$(grep -B5 comm_http.txt $i | awk -F"server_name" '{print $2}' | tr " " "\n" | grep -P "^[a-zA-Z0-9-]+\.[a-zA-Z]+$" | sort | uniq | wc -l)
    ### 现金网https的裸域名个数统计
    Https_Count=$(grep -B5 comm_https.txt $i | awk -F"server_name" '{print $2}' | tr " " "\n" | grep -P "^[a-zA-Z0-9-]+\.[a-zA-Z]+$" | sort | uniq | wc -l)
    ### 跳过没有包含comm_http.txt 和 comm_https.txt配置
    [[ $Http_Count -eq 0 && $Https_Count -eq 0 ]] && continue
    ### 从incap-api文件中查找某个现金网的源ip
    IP=$(grep -A4 "domain ${Client_Name}01.lebosys.com" $Incap_File | grep ips | sed -e 's/ips \[204.128.57.//; s/\]//')
    ### 如果没有查到源ip 设为空
    [ -z $IP ] && Origin_Server_Name="" || Origin_Server_Name="twdl$IP-$Client_Name"
    [ -z $IP ] && Origin_Server_Ip=""   || Origin_Server_Ip="204.128.57.$IP"
    ### 查找https配置段个数
    aa=($(awk '/comm_https.txt/ {print NR}' $i))
    ### 是否在incapsula上
    Old_Cname="${Client_Name}.leboweb.com"
    [ "${Client_Name}" == "95zz" ] && Old_Cname="bbet888.leboweb.com"
    [ "${Client_Name}" == "hsdc" ] && Old_Cname="hsdc888.leboweb.com"
    [ "${Client_Name}" == "test" ] && Old_Cname="test.lebosys.com"
    ping -c 1 ${Old_Cname} | grep incapdns.net > /dev/null && Location="YES" || Location="<font color='red'>NO</font>"
    ### 如果https配置段为空
    if [ -z $aa ] ; then
        Location="<font color='blue'>${Location}</font>"
        Origin_Server_Name="twdl199-allhttp"
        Origin_Server_Ip="204.128.57.199"
        Site_Name_Http="80.lebosys.com"
        Site_Id_Http=$(grep -B2 "domain $Site_Name_Http" $Incap_File | awk '$0~/site_id/{print $NF}')
        Incap_Cname_Http=$(grep -A9 "domain $Site_Name_Http" $Incap_File | grep set_data_to | sed 's/set_data_to \[//; s/\]\}\]//')
        echo "
   <tr>
    <td><center>${Client_Name}</center></td>
    <td><center>${Location}</center></td>
    <td><center><font color='blue'>${Origin_Server_Name}</font></center></td>
    <td><center><font color='blue'>${Origin_Server_Ip}</font></center></td>
    <td><center>${Http_Count}</center></td>
    <td><center>${Https_Count}</center></td>
    <td><center> </center></td>
    <td><center> </center></td>
    <td><center> </center></td>
    <td><center> </center></td>
    <td><center> </center></td>
    <td><center><font color='blue'>${Site_Name_Http}</font></center></td>
    <td><center><font color='blue'>${Site_Id_Http}</font></center></td>
    <td><center><font color='blue'>${Incap_Cname_Http}</font></center></td>
   </tr>" > ${Incap_Html_Tmp}_80_${Client_Name}
    ### 如果https配置段不为空
    else
        Arrow_Number=0
        ### 每个https段配置裸域名的个数Domain_Count_Tmp数组、证书首域名First_Domain_Tmp数组
        for j in ${aa[@]}
        do
            bb=$(($j - 5))
            cc=$(sed -n "$bb,$j p" $i | awk -F"server_name" '{print $2}' | tr " " "\n" | grep -P "^[a-zA-Z0-9-]+\.[a-zA-Z]+$" | sort | uniq | wc -l)
            Domain_Count_Tmp[$Arrow_Number]=$cc
            dd=$(sed -n "$bb,$j p" $i | grep -w ssl_certificate | awk -F"/" '{print $NF}' | awk -F".crt" '{print $1}')
            First_Domain_Tmp[$Arrow_Number]=$dd
            Arrow_Number=$(( $Arrow_Number + 1 ))
        done
        ### 确定Site_Name数组，初步确定First_Domain_Curl数组，Site_Id数组，Incap_Cname数组
        for (( k=0; k<"$Arrow_Number"; k=k+1 ))
        do
            Count=$(( $k + 1))
            [ $Count -lt 10 ] && ee="${Client_Name}0${Count}.lebosys.com" || ee="${Client_Name}${Count}.lebosys.com"
            [ $Client_Name == "test" ] && ee="test.lebosys.com" && Origin_Server_Name="twdl200-lebotest" && Origin_Server_Ip="204.128.57.200"
            Site_Name[$k]=$ee
            First_Domain_Curl[$k]=$(curl -v https://${Site_Name[$k]} 2>&1 | awk '/common name/ {print $4}' | grep -vE "lebosys.com|incapsula.com")
            ff=$(grep -B2 "domain $ee" $Incap_File | awk '$0~/site_id/{print $NF}')
            Site_Id[$k]=$ff
            gg=$(grep -A9 "domain $ee" $Incap_File | grep set_data_to | sed 's/set_data_to \[//; s/\]\}\]//')
            Incap_Cname[$k]=$gg
        done
        ### 
        aaa=0
        for (( kk=0; kk<"$Arrow_Number"; kk=kk+1 ))
        do
            flags=0
            for i in ${First_Domain_Tmp[@]}
            do
                if [ "$i" == "${First_Domain_Curl[$kk]}" ] ; then
                    flags=1
                    break
                else
                    flags=0
                fi
            done
            if [[ $flags -eq 0 || -z ${First_Domain_Curl[$kk]} ]] ; then
                Number_Zero[$aaa]=$kk
                aaa=$(($aaa + 1))
            else
                First_Domain[$kk]=${First_Domain_Curl[$kk]}
                Domain_Count[$kk]=${Domain_Count_Tmp[$kk]}
            fi
        done
        ### 
        t=0
        flag=0
        for (( kkk=0; kkk<"$Arrow_Number"; kkk=kkk+1 ))
        do
            for m in "${First_Domain_Curl[@]}"
            do
                if [ "${First_Domain_Tmp[$kkk]}" == "$m" ] ; then
                    flag=1
                    break
                fi
            done
            if [ $flag -eq 0 ] ; then
                result_list[t]=${First_Domain_Tmp[$kkk]}
                result_cout[t]=${Domain_Count_Tmp[$kkk]}
                t=$(($t+1))
            else
                flag=0
            fi
        done
        ###
        for (( mm=0; mm<$t; mm++ ))
        do
            First_Domain[${Number_Zero[$mm]}]=${result_list[$mm]}
            Domain_Count[${Number_Zero[$mm]}]=${result_cout[$mm]}
        done
        ###
        Tmp_Ip=${Origin_Server_Ip}
        Tmp_Name=${Client_Name}
        > ${Incap_Html_Tmp}_${Tmp_Ip}_${Tmp_Name}
        for (( m=0; m<"$Arrow_Number"; m=m+1 ))
        do
            Crt_File=$(find /usr/local/openresty/nginx/conf/ -name "${First_Domain[$m]}.crt" | head -1)
            Local_Crt_Start=$(openssl x509 -startdate -noout -in "${Crt_File}" | sed -e 's/  / 0/;s/notBefore=//')
            Local_Crt_End=$(openssl x509 -enddate -noout -in "${Crt_File}" | sed -e 's/  / 0/;s/notAfter=//')

            Now_Second=$(date +%s)
            End_Second=$(date +%s -d "${Local_Crt_End}")
            Remain_Second=$(expr ${End_Second} - ${Now_Second})
            Remain_Day=$(expr ${Remain_Second} / 86400)

            First_Domain_Start[$m]=$(date +%F/%T -d "${Local_Crt_Start}")
            First_Domain_End[$m]=$(date +%F -d "${Local_Crt_End}")
            First_Domain_Remain[$m]=${Remain_Day}

            if [ -z ${Site_Id[$m]} ] ; then
                ping -c 1 "${Client_Name}.lebosys.com" > /root/.ping_tmp_${Client_Name}
                Ping_Flag=$(echo $?)
                IP=$(awk '/^PING/{print $3}' /root/.ping_tmp_${Client_Name} | cut -c 13-15)
                if [[ -z ${IP} || ${IP} -eq 200 ]] ; then
                    Origin_Server_Name=""
                    Origin_Server_Ip=""
                else
                    Origin_Server_Name="twdl$IP-$Client_Name"
                    Origin_Server_Ip="204.128.57.$IP"
                    [ ${Ping_Flag} -ne 0 ] && Origin_Server_Name="<font color='RED'>${Origin_Server_Name}</font>" && Origin_Server_Ip="<font color='RED'>${Origin_Server_Ip}</font>"
                fi
                Site_Name[$m]="<font color='RED'>${Site_Name[$m]}</font>"
            else
                Curl_Temp=$(curl -vI https://${Site_Name[$m]} 2>&1 | awk '/common name/ {print $4}' | grep -vE "lebosys.com|incapsula.com")
                Incap_Crt_Start=$(curl -vI https://${Site_Name[$m]} 2>&1 | grep 'start date' | sed 's/\* \tstart date: //')
                Key_File=$(find /usr/local/openresty/nginx/conf -name "${First_Domain[$m]}.key" | head -1)
                if [[ "${First_Domain[$m]}" != "${Curl_Temp}" || "${Local_Crt_Start}" != "${Incap_Crt_Start}" ]] ; then
                    echo -e "${First_Domain[$m]} \t ${Curl_Temp} \t ${Local_Crt_Start} \t ${Incap_Crt_Start}"
                    CERT_B64=`base64 -i ${Crt_File}`
                    KEY_B64=`base64 -i  ${Key_File}`
                    curl -d api_id=23304 -d api_key=4088fa23-c869-46ad-994b-3771cdf76f08 -d site_id=${Site_Id[$m]} \
                        -d certificate="$CERT_B64" -d private_key="$KEY_B64" \
                        https://my.incapsula.com/api/prov/v1/sites/customCertificate/upload
                fi

                if [[ ${Site_Name[$m]} =~ 01.lebosys.com ]] ; then
                    Location="<font color='green'>${Location}</font>" 
                    Site_Name[$m]="<font color='green'>${Site_Name[$m]}</font>"
                    Site_Id[$m]="<font color='green'>${Site_Id[$m]}</font>"
                    Incap_Cname[$m]="<font color='green'>${Incap_Cname[$m]}</font>"
                fi
            fi
            if [[ ${Site_Name[$m]} != *01.lebosys.com ]] ; then
                Client_Name=""
                Location=""
                Origin_Server_Name=""
                Origin_Server_Ip=""
                Http_Count=""
                Https_Count=""
            fi
            echo "
   <tr>
    <td><center>${Client_Name}</center></td>
    <td><center>${Location}</center></td>
    <td><center>${Origin_Server_Name}</center></td>
    <td><center>${Origin_Server_Ip}</center></td>
    <td><center>${Http_Count}</center></td>
    <td><center>${Https_Count}</center></td>
    <td><center>${First_Domain[$m]}</center></td>
    <td><center>${Domain_Count[$m]}</center></td>
    <td><center>${First_Domain_Start[$m]}</center></td>
    <td><center>${First_Domain_End[$m]}</center></td>
    <td><center>${First_Domain_Remain[$m]}</center></td>
    <td><center>${Site_Name[$m]}</center></td>
    <td><center>${Site_Id[$m]}</center></td>
    <td><center>${Incap_Cname[$m]}</center></td>
   </tr>" >> ${Incap_Html_Tmp}_${Tmp_Ip}_${Tmp_Name}
        done
    fi
} &
done

wait

cat ${Incap_Html_Tmp}_* >> ${Incap_Html_Tmp}

echo "
  </table>
 </body>
</html>" >> ${Incap_Html_Tmp}
sed -i "s/ End_Time/ $(date '+%F %T') AMT/" ${Incap_Html_Tmp}
\cp ${Incap_Html_Tmp} ${Incap_Html}
rm -f ${Incap_Html_Tmp}_* /root/.ping_tmp_*