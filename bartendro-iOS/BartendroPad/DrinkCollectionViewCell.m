//
//  DrinkCollectionViewCell.m
//  BartendroPad
//
//  Created by Pablo Castro on 12/11/13.
//  Copyright (c) 2013 witty. All rights reserved.
//

#import "DrinkCollectionViewCell.h"

@implementation DrinkCollectionViewCell

@synthesize drink;


- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        // Initialization code
    }
    return self;
}

/*
// Only override drawRect: if you perform custom drawing.
// An empty implementation adversely affects performance during animation.
- (void)drawRect:(CGRect)rect
{
    // Drawing code
}
*/

-(void)populateUIwithDatafrom:(Drink *)aDrink{

    self.backgroundColor = [UIColor whiteColor];
    self.drinkDescription.text = aDrink.desc;
    self.drinkName.text = aDrink.name;
    
    [self setDrink:aDrink];

}


- (IBAction)pourDrink:(id)sender {
    
    NSLog(@"Pouring a drink called: %@", self.drink.name);
    
}
@end
