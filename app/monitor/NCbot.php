<?php
include('../config/config.php');

	function NextcloudTalk_SendMessage($channel_id, $message) {
		// notify hack
		$data = array(
			"token" => $channel_id,
			"message" => $message
		);

		$payload = json_encode($data);

		$ch = curl_init($SERVER . '/ocs/v2.php/apps/spreed/api/v1/chat/' . $channel_id);

		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLINFO_HEADER_OUT, true);
		curl_setopt($ch, CURLOPT_POST, true);
		curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
		curl_setopt($ch, CURLOPT_USERPWD, "$USER:$PASS");
		curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);

		// Set HTTP Header
		curl_setopt($ch, CURLOPT_HTTPHEADER, array(
			'Content-Type: application/json',
			'Content-Length: ' . strlen($payload),
			'Accept: application/json',
			'OCS-APIRequest: true')
		);

		$result = curl_exec($ch);
		curl_close($ch);

	}

	$token = $argv[1];
	$message = $argv[2];

	NextcloudTalk_SendMessage($token, $message);
?>
