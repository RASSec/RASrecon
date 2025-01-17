<?php
/**
 * This script is only runnable form command line
 */
if (substr(php_sapi_name(), 0, 3) != 'cli'):
    die('This script can only be run from command line!');
endif;
/**
 * Convert seconds to minutes, hours..
 * NOTICE : Approximate, assumes months have 30 days.
 */
function seconds2human($ss)
{
    $s = $ss%60;
    $mins = floor(($ss%3600)/60);
    $hours = floor(($ss%86400)/3600);
    $days = floor(($ss%2592000)/86400);
    $months = floor($ss/2592000);
    $text = '';
    if ($months > 0) {
        $text .= $months." months,";
    }
    if ($days > 0) {
        $text .= $days." days,";
    }
    if ($hours > 0) {
        $text .= $hours." hours,";
    }
    if ($mins > 0) {
        $text .= $mins." minutes,";
    }
    if ($s > 0) {
        $text .= $s." seconds";
    }
    return $text;
}

/**
 * Magic starts here
 */
$start_ts = time();
if (!isset($argv[1])):
	die('Please provide a file name to import!'."\n");
endif;
$tmp = pathinfo($argv[1]);
if ($tmp['dirname'] == "."):
	$filepath = dirname(__FILE__).'/'.$argv[1];
else:
	$filepath = $argv[1];
endif;
if (!is_file($filepath)):
	echo "File:".$filepath;
	echo PHP_EOL;
	echo 'File does not exist!';
    echo PHP_EOL;
	exit;
endif;

echo "Reading file";
echo PHP_EOL;
$content =  utf8_encode(file_get_contents($filepath));
echo "Parsing file";
echo PHP_EOL;
$xml = simplexml_load_string($content, 'SimpleXMLElement', LIBXML_COMPACT | LIBXML_PARSEHUGE);
if ($xml === false):
    die('There is a problem with this xml file?!'.PHP_EOL);
endif;
$total		= 0;
$inserted	= 0;
echo "Processing data (This may take some time depending on file size)";
echo PHP_EOL;
foreach ($xml->host as $host):
	$AA=array();
	foreach ($host->ports as $p):
        $ip = $host->address['addr'];
        @file_put_contents("report/result_sentives.html", '<h2><font color=red>'.$ip.'</font></h2>', FILE_APPEND);
		print $ip.'<br>';
		foreach ($p->port as $pp){
			$p_protocol=$pp['protocol'];
			$p_port=(int)$pp['portid'];
			$p_service_http_title=$pp->script["http-title"]['output'];			
			$p_banner=$pp->script['output'];
			$p_service=$pp->service["name"];
			$total++;
			$fwritt='<b>'.$p_protocol.'</b>   '.'<a href="http://'.$ip.':'.$p_port.'"" target=_blank><b>'.$p_port.'</b></a>'.'   <b>'.$p_service.'</b>   <pre>'.$p_service_http_title.'</pre>   <pre>'.$p_banner.'</pre>   '.'   '.'<br>';
            print $fwritt;
            @file_put_contents("report/result_sentives.html", $fwritt, FILE_APPEND);
			}

	endforeach;
endforeach;
$end_ts = time();
echo PHP_EOL;
echo "Summary:";
echo PHP_EOL;
echo "Total records:".$total."\n";
echo "Inserted records:".$inserted."\n";
$secs = $end_ts - $start_ts;
echo "Took about:".seconds2human($secs);
echo PHP_EOL;
