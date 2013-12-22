//
//  Drink.h
//  BartendroPad
//
//  Created by Pablo Castro on 12/3/13.
//  Copyright (c) 2013 witty. All rights reserved.
//

#import <Foundation/Foundation.h>
//#import <CoreData/CoreData.h>


@interface Drink : NSObject

@property (nonatomic, retain) NSNumber * drink_id;
@property (nonatomic, retain) NSString * desc;
@property (nonatomic, retain) NSNumber * name_id;

@property (nonatomic, retain) NSString * name;

@property (nonatomic, retain) NSNumber * sugg_size;
@property (nonatomic, retain) NSNumber * popular;
@property (nonatomic, retain) NSNumber * available;
@property (nonatomic, retain) NSDictionary * info;

@end
