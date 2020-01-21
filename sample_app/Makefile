build:
	xcrun xcodebuild  -scheme SampleApp -sdk iphoneos DEVELOPMENT_TEAM="39WPV9Z5KK" -destination generic/platform=iOS clean build
	xcrun xcodebuild  -scheme SampleApp -sdk iphoneos DEVELOPMENT_TEAM="39WPV9Z5KK" -configuration AppStoreDistribution archive -archivePath $PWD/SampleApp.xcarchive
	xcodebuild -exportArchive -archivePath $PWD/SampleApp.xcarchive -exportOptionsPlist exportOptions.plist -exportPath $PWD/