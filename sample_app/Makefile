
all: clean ios_build

clean:
	xcrun xcodebuild  -scheme SampleApp -sdk iphoneos DEVELOPMENT_TEAM="$(DEVELOPMENT_TEAM)" -destination generic/platform=iOS clean

ios_build:
	sed 's/__DEVELOPMENT_TEAM__/$(DEVELOPMENT_TEAM)/g' exportOptions.plist.template > exportOptions.plist
	xcrun xcodebuild  -scheme SampleApp -sdk iphoneos DEVELOPMENT_TEAM="$(DEVELOPMENT_TEAM)" -destination generic/platform=iOS build
	xcrun xcodebuild  -scheme SampleApp -sdk iphoneos DEVELOPMENT_TEAM="$(DEVELOPMENT_TEAM)" -configuration AppStoreDistribution archive -archivePath build/SampleApp.xcarchive
	xcodebuild -allowProvisioningUpdates -exportArchive -archivePath build/SampleApp.xcarchive -exportOptionsPlist exportOptions.plist -exportPath build
